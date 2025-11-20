"""
TTS Engine — Audio Provider Interface

This module defines the abstract base class that all TTS providers must implement.
It establishes a contract for voice generation, ensuring consistent behavior across
different engines (local, remote, hybrid).

Design Philosophy:
- Provider-agnostic: The Director doesn't care if audio comes from Piper or ElevenLabs
- Content-addressable: Providers hash inputs to enable intelligent caching
- Configuration-driven: Each provider accepts engine-specific configs from the manifest
- Quality-aware: Providers report quality metrics for monitoring
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any
import hashlib
import json


@dataclass
class AudioGenerationRequest:
    """
    Encapsulates all information needed to generate speech.

    This structure is hashed to create cache keys, ensuring identical
    requests return cached results instead of re-generating.
    """
    text: str                          # The script to speak
    voice_id: str                      # Voice identifier (name, path to .pth, etc.)
    language: str = "en"               # Language code
    speed: float = 1.0                 # Playback speed multiplier
    temperature: float = 0.7           # Sampling temperature (expressiveness)
    emotion: Optional[str] = None      # Emotion tag (if supported)
    style: Optional[str] = None        # Speaking style (narrative, conversational, etc.)
    extra_config: Dict[str, Any] = None  # Provider-specific parameters

    def to_cache_key(self) -> str:
        """
        Generate deterministic hash for caching.

        Returns:
            SHA256 hash of request parameters
        """
        # Sort dict keys for deterministic serialization
        payload = {
            "text": self.text,
            "voice_id": self.voice_id,
            "language": self.language,
            "speed": self.speed,
            "temperature": self.temperature,
            "emotion": self.emotion,
            "style": self.style,
            "extra_config": self.extra_config or {}
        }
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()


@dataclass
class AudioGenerationResult:
    """
    Result of an audio generation request.

    Includes quality metrics for monitoring and fallback logic.
    """
    audio_path: Path                   # Absolute path to generated .wav/.mp3
    duration_seconds: float            # Audio duration
    sample_rate: int                   # Sample rate (Hz)
    was_cached: bool                   # True if returned from cache
    generation_time_seconds: float     # Time spent generating (0 if cached)
    quality_score: Optional[float] = None  # 0-1 quality metric (if measurable)
    provider_name: str = "unknown"     # Which provider generated this


class AudioProvider(ABC):
    """
    Abstract base class for all TTS providers.

    Concrete implementations:
    - LocalPiperProvider: Fast, CPU-friendly inference
    - LocalXTTSProvider: High-quality, GPU-accelerated
    - ColabXTTSProvider: Remote GPU worker via ngrok
    - HybridProvider: Intelligent routing based on load/quality needs
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize provider with configuration from manifest.

        Args:
            config: Engine-specific parameters (temperature, voice paths, API keys, etc.)
        """
        self.config = config
        self.provider_name = self.__class__.__name__

    @abstractmethod
    def generate(self, request: AudioGenerationRequest) -> AudioGenerationResult:
        """
        Generate speech audio from text.

        Implementations MUST:
        1. Check cache before generating (via AssetManager)
        2. Generate audio if cache miss
        3. Save to content-addressed path
        4. Return AudioGenerationResult with metrics

        Args:
            request: Audio generation parameters

        Returns:
            AudioGenerationResult with path to generated audio

        Raises:
            AudioGenerationError: If generation fails
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if this provider can currently generate audio.

        Examples:
        - LocalProvider: Check if models are downloaded
        - ColabProvider: Ping ngrok endpoint
        - HybridProvider: Check if fallback is available

        Returns:
            True if provider is ready to generate
        """
        pass

    @abstractmethod
    def warmup(self) -> None:
        """
        Preload models into memory (if applicable).

        Called once at startup to avoid cold-start latency
        on first generation request.
        """
        pass

    def estimate_generation_time(self, text_length: int) -> float:
        """
        Estimate how long generation will take (optional).

        Used by HybridProvider to decide between local and remote.

        Args:
            text_length: Number of characters in input text

        Returns:
            Estimated seconds to generate (0 if unknown)
        """
        return 0.0

    def supports_voice_cloning(self) -> bool:
        """Whether this provider can clone voices from samples."""
        return False

    def supports_emotion_control(self) -> bool:
        """Whether this provider accepts emotion parameters."""
        return False


class AudioGenerationError(Exception):
    """Raised when TTS generation fails."""
    pass
