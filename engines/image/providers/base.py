"""
Base classes for Image Generation providers.

This module defines the abstract interface that all image generation
providers must implement, ensuring consistent behavior across different
backends (DALL-E, Stable Diffusion, Midjourney, etc.).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, List
import hashlib


@dataclass
class ImageGenerationRequest:
    """Request for image generation"""
    prompt: str
    negative_prompt: Optional[str] = None
    width: int = 1024
    height: int = 1024
    style: Optional[str] = None  # documentary, cinematic, photorealistic, etc.
    seed: Optional[int] = None
    guidance_scale: float = 7.5
    num_inference_steps: int = 50

    def to_cache_key(self) -> str:
        """Generate unique cache key from request parameters"""
        components = [
            self.prompt,
            self.negative_prompt or "",
            str(self.width),
            str(self.height),
            self.style or "",
            str(self.seed) if self.seed else "",
            str(self.guidance_scale),
            str(self.num_inference_steps)
        ]
        return hashlib.sha256("|".join(components).encode()).hexdigest()


@dataclass
class ImageGenerationResult:
    """Result from image generation"""
    image_path: Path
    was_cached: bool = False
    generation_time: float = 0.0
    quality_score: Optional[float] = None  # 0-1 scale
    provider_name: str = "unknown"
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ImageProvider(ABC):
    """
    Abstract base class for all image generation providers.

    Providers handle image generation from text prompts with support for:
    - Multiple aspect ratios and resolutions
    - Style control (documentary, cinematic, etc.)
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
    def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        """
        Generate image from text prompt.

        Args:
            request: Image generation request with prompt and parameters

        Returns:
            ImageGenerationResult with path to generated image

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if provider is available and ready to use.

        Returns:
            True if provider can generate images, False otherwise
        """
        pass

    def warmup(self) -> None:
        """
        Optional warmup/initialization (load models, test connection, etc.).

        Default implementation does nothing. Override if needed.
        """
        pass

    def get_supported_resolutions(self) -> List[tuple[int, int]]:
        """
        Get list of supported (width, height) resolutions.

        Returns:
            List of (width, height) tuples
        """
        return [
            (1024, 1024),  # Square
            (1920, 1080),  # 16:9 landscape
            (1080, 1920),  # 9:16 portrait
            (1280, 720),   # 16:9 HD
        ]

    def validate_request(self, request: ImageGenerationRequest) -> bool:
        """
        Validate image generation request parameters.

        Args:
            request: Request to validate

        Returns:
            True if valid, False otherwise
        """
        if not request.prompt or len(request.prompt.strip()) == 0:
            return False

        if request.width <= 0 or request.height <= 0:
            return False

        if request.guidance_scale < 0:
            return False

        return True
