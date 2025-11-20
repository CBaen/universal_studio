"""
Base classes for Video Assembly/Rendering providers.

This module defines the abstract interface that all video assembly
providers must implement. Video engine focuses on final assembly,
compositing, and rendering rather than generation.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, List
import hashlib


@dataclass
class VideoScene:
    """Single scene in the video timeline"""
    audio_path: Path
    image_path: Optional[Path] = None
    duration: float = 0.0  # Derived from audio if not specified
    transition: str = "fade"  # fade, cut, dissolve, etc.
    effects: List[str] = None  # zoom, pan, ken_burns, etc.

    def __post_init__(self):
        if self.effects is None:
            self.effects = []


@dataclass
class VideoAssemblyRequest:
    """Request for video assembly"""
    scenes: List[VideoScene]
    title: Optional[str] = None
    resolution: tuple[int, int] = (1920, 1080)  # width, height
    fps: int = 30
    format: str = "mp4"
    codec: str = "h264"
    quality: str = "high"  # low, medium, high, max
    background_music_path: Optional[Path] = None
    background_music_volume: float = 0.3

    def to_cache_key(self) -> str:
        """Generate unique cache key from request parameters"""
        scene_hashes = [
            f"{s.audio_path}|{s.image_path}|{s.duration}"
            for s in self.scenes
        ]
        components = [
            "|".join(scene_hashes),
            self.title or "",
            f"{self.resolution[0]}x{self.resolution[1]}",
            str(self.fps),
            self.format,
            self.codec,
            self.quality,
        ]
        return hashlib.sha256("|".join(components).encode()).hexdigest()


@dataclass
class VideoAssemblyResult:
    """Result from video assembly"""
    video_path: Path
    was_cached: bool = False
    assembly_time: float = 0.0
    duration: float = 0.0
    file_size: int = 0  # bytes
    provider_name: str = "unknown"
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class VideoProvider(ABC):
    """
    Abstract base class for all video assembly providers.

    Providers handle video assembly/rendering with support for:
    - Multi-scene timeline composition
    - Transition effects (fade, dissolve, cut)
    - Visual effects (zoom, pan, ken burns)
    - Background music mixing
    - Multiple resolutions and formats
    - Hardware acceleration (GPU encoding)
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
    def assemble(self, request: VideoAssemblyRequest) -> VideoAssemblyResult:
        """
        Assemble video from scenes and audio.

        Args:
            request: Video assembly request with scenes and parameters

        Returns:
            VideoAssemblyResult with path to rendered video

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if provider is available and ready to use.

        Returns:
            True if provider can assemble videos, False otherwise
        """
        pass

    def warmup(self) -> None:
        """
        Optional warmup/initialization (test ffmpeg, GPU check, etc.).

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
            (1920, 1080),  # 1080p
            (2560, 1440),  # 1440p
            (3840, 2160),  # 4K
            (1280, 720),   # 720p
        ]

    def get_supported_formats(self) -> List[str]:
        """
        Get list of supported output formats.

        Returns:
            List of format names
        """
        return ["mp4", "mov", "webm", "avi"]

    def validate_request(self, request: VideoAssemblyRequest) -> bool:
        """
        Validate video assembly request parameters.

        Args:
            request: Request to validate

        Returns:
            True if valid, False otherwise
        """
        if not request.scenes or len(request.scenes) == 0:
            return False

        # Validate all scenes have audio
        for scene in request.scenes:
            if not scene.audio_path or not scene.audio_path.exists():
                return False

        if request.fps <= 0 or request.fps > 120:
            return False

        return True

    def estimate_render_time(self, request: VideoAssemblyRequest) -> float:
        """
        Estimate rendering time in seconds.

        Args:
            request: Video assembly request

        Returns:
            Estimated time in seconds
        """
        # Simple heuristic: 1x real-time for high quality
        total_duration = sum(s.duration for s in request.scenes)
        quality_multiplier = {
            "low": 0.3,
            "medium": 0.5,
            "high": 1.0,
            "max": 2.0,
        }.get(request.quality, 1.0)

        return total_duration * quality_multiplier
