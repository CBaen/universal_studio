"""
Base classes for Sound Effects (SFX) Generation providers.

This module defines the abstract interface that all sound effects generation
providers must implement, ensuring consistent behavior across different
backends (AudioLDM, AudioGen, Freesound API, etc.).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, List
import hashlib


@dataclass
class SFXGenerationRequest:
    """Request for sound effect generation"""
    prompt: str
    duration: float = 5.0  # seconds
    category: Optional[str] = None  # ambient, impact, transition, etc.
    intensity: Optional[str] = None  # subtle, moderate, dramatic
    environment: Optional[str] = None  # indoor, outdoor, urban, nature
    seed: Optional[int] = None

    def to_cache_key(self) -> str:
        """Generate unique cache key from request parameters"""
        components = [
            self.prompt,
            str(self.duration),
            self.category or "",
            self.intensity or "",
            self.environment or "",
            str(self.seed) if self.seed else "",
        ]
        return hashlib.sha256("|".join(components).encode()).hexdigest()


@dataclass
class SFXGenerationResult:
    """Result from sound effect generation"""
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


class SFXProvider(ABC):
    """
    Abstract base class for all sound effects generation providers.

    Providers handle SFX generation from text prompts with support for:
    - Category control (ambient, impact, transition)
    - Intensity levels (subtle to dramatic)
    - Environment characteristics
    - Variable duration (0.5s to 30s)
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
    def generate(self, request: SFXGenerationRequest) -> SFXGenerationResult:
        """
        Generate sound effect from text prompt.

        Args:
            request: SFX generation request with prompt and parameters

        Returns:
            SFXGenerationResult with path to generated audio

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if provider is available and ready to use.

        Returns:
            True if provider can generate SFX, False otherwise
        """
        pass

    def warmup(self) -> None:
        """
        Optional warmup/initialization (load models, test connection, etc.).

        Default implementation does nothing. Override if needed.
        """
        pass

    def get_supported_categories(self) -> List[str]:
        """
        Get list of supported SFX categories.

        Returns:
            List of category names
        """
        return [
            "ambient",      # Background atmosphere
            "impact",       # Sudden sounds (door slam, gunshot)
            "transition",   # Scene change sounds (whoosh, swoosh)
            "foley",        # Human actions (footsteps, typing)
            "nature",       # Environmental (wind, rain, birds)
            "urban",        # City sounds (traffic, sirens)
            "mechanical",   # Machines (engines, clicks)
        ]

    def get_max_duration(self) -> float:
        """
        Get maximum supported audio duration in seconds.

        Returns:
            Maximum duration in seconds
        """
        return 30.0  # 30 seconds default for SFX

    def validate_request(self, request: SFXGenerationRequest) -> bool:
        """
        Validate SFX generation request parameters.

        Args:
            request: Request to validate

        Returns:
            True if valid, False otherwise
        """
        if not request.prompt or len(request.prompt.strip()) == 0:
            return False

        if request.duration <= 0 or request.duration > self.get_max_duration():
            return False

        return True
