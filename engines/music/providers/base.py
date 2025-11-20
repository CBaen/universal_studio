"""
Base classes for Music Generation providers.

This module defines the abstract interface that all music generation
providers must implement, ensuring consistent behavior across different
backends (MusicGen, AudioCraft, Suno API, etc.).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, List
import hashlib


@dataclass
class MusicGenerationRequest:
    """Request for music generation"""
    prompt: str
    duration: float = 30.0  # seconds
    genre: Optional[str] = None  # ambient, dramatic, suspenseful, etc.
    mood: Optional[str] = None  # dark, mysterious, uplifting, etc.
    tempo: Optional[int] = None  # BPM
    key: Optional[str] = None  # C major, A minor, etc.
    instrumentation: Optional[str] = None
    seed: Optional[int] = None

    def to_cache_key(self) -> str:
        """Generate unique cache key from request parameters"""
        components = [
            self.prompt,
            str(self.duration),
            self.genre or "",
            self.mood or "",
            str(self.tempo) if self.tempo else "",
            self.key or "",
            self.instrumentation or "",
            str(self.seed) if self.seed else "",
        ]
        return hashlib.sha256("|".join(components).encode()).hexdigest()


@dataclass
class MusicGenerationResult:
    """Result from music generation"""
    audio_path: Path
    was_cached: bool = False
    generation_time: float = 0.0
    quality_score: Optional[float] = None  # 0-1 scale
    provider_name: str = "unknown"
    actual_duration: float = 0.0
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class MusicProvider(ABC):
    """
    Abstract base class for all music generation providers.

    Providers handle music generation from text prompts with support for:
    - Genre and mood control
    - Tempo and key specification
    - Variable duration (5s to 5min+)
    - Quality scoring and validation
    - Local caching for efficiency
    """

    def __init__(self, config: dict):
        """
        Initialize provider with configuration.

        Args:
            config: Provider-specific configuration dictionary
        """
        self.config = config
        self.cache_dir = Path(config.get("cache_dir", "./cache"))
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def generate(self, request: MusicGenerationRequest) -> MusicGenerationResult:
        """
        Generate music from text prompt.

        Args:
            request: Music generation request with prompt and parameters

        Returns:
            MusicGenerationResult with path to generated audio

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if provider is available and ready to use.

        Returns:
            True if provider can generate music, False otherwise
        """
        pass

    def warmup(self) -> None:
        """
        Optional warmup/initialization (load models, test connection, etc.).

        Default implementation does nothing. Override if needed.
        """
        pass

    def get_supported_genres(self) -> List[str]:
        """
        Get list of supported music genres.

        Returns:
            List of genre names
        """
        return [
            "ambient",
            "cinematic",
            "dramatic",
            "suspenseful",
            "mysterious",
            "uplifting",
            "dark",
            "documentary",
        ]

    def get_max_duration(self) -> float:
        """
        Get maximum supported audio duration in seconds.

        Returns:
            Maximum duration in seconds
        """
        return 300.0  # 5 minutes default

    def validate_request(self, request: MusicGenerationRequest) -> bool:
        """
        Validate music generation request parameters.

        Args:
            request: Request to validate

        Returns:
            True if valid, False otherwise
        """
        if not request.prompt or len(request.prompt.strip()) == 0:
            return False

        if request.duration <= 0 or request.duration > self.get_max_duration():
            return False

        if request.tempo and (request.tempo < 20 or request.tempo > 300):
            return False

        return True
