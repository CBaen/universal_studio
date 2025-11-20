"""
Render Manifest data models.

Python dataclasses matching Gemini's TypeScript schema for the RenderManifest.
This is the contract between Gemini (Showrunner) and Claude (Production Engine).
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from datetime import datetime


# Enums matching TypeScript definitions

class MediaType(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"


class Genre(str, Enum):
    MYSTERY = "Mystery / Thriller"
    TRUE_CRIME = "True Crime"
    HISTORY = "Historical Documentary"
    TECH_NEWS = "Tech News / Update"
    EDUCATIONAL = "Educational / Explainer"
    COMEDY = "Comedy / Satire"
    HORROR = "Cosmic Horror"
    CORPORATE = "Corporate Presentation"
    SCIFI = "Sci-Fi / Speculative"


class VisualStyle(str, Enum):
    PHOTOREALISTIC = "Cinematic Photorealistic"
    VINTAGE_FILM = "Vintage 35mm Film"
    ANIME = "Anime / 2D Animation"
    CYBERPUNK = "Neon Cyberpunk / Sci-Fi"
    CLAYMATION = "Claymation / Stop Motion"
    MINIMALIST = "Minimalist Vector Art"
    SKETCH = "Charcoal Sketch"
    VHS = "VHS / Glitch Art"
    DATA_VIZ = "Abstract Data Visualization"


class VoicePersona(str, Enum):
    FENRIR = "Fenrir (Deep, Thriller, Authoritative)"
    ZEPHYR = "Zephyr (Calm, Friendly, Narrator)"
    KORE = "Kore (Soft, Relaxing, Bedtime)"
    PUCK = "Puck (Energetic, Playful, Comedy)"
    CHARON = "Charon (Deep, Gravelly, Horror)"
    ATLAS = "Atlas (Confident, News Anchor)"
    LUNA = "Luna (Mysterious, Whispery)"


class AudioMood(str, Enum):
    SUSPENSE = "Suspenseful (Eerie, Low drones)"
    MELANCHOLIC = "Melancholic (Piano, Rain, Somber)"
    FUTURISTIC = "Futuristic (Synth, Glitch, Digital)"
    NATURE = "Nature (Wind, Birds, Flowing water)"
    INTENSE = "Intense (Heartbeat, Riser, Tense)"
    UPBEAT = "Upbeat (Light, Inspiring)"
    CORPORATE = "Corporate (Clean, Driving, Minimal)"
    DARK_AMBIENT = "Dark Ambient (Space, Void)"


class AspectRatio(str, Enum):
    WIDE_16_9 = "16:9"
    PORTRAIT_9_16 = "9:16"
    SQUARE_1_1 = "1:1"
    STANDARD_4_3 = "4:3"


class TransitionType(str, Enum):
    CUT = "Cut"
    FADE_TO_BLACK = "Fade to Black"
    CROSS_DISSOLVE = "Cross Dissolve"
    WIPE = "Wipe"
    ZOOM_IN = "Zoom In"
    GLITCH = "Glitch"


class KenBurnsEffect(str, Enum):
    ZOOM_IN = "Zoom In"
    ZOOM_OUT = "Zoom Out"
    PAN_LEFT = "Pan Left"
    PAN_RIGHT = "Pan Right"
    STATIC = "Static"


Platform = Literal["youtube", "tiktok", "facebook", "spotify", "patreon"]
RenderResolution = Literal["720p", "1080p", "4k"]
ExportType = Literal["video_full", "video_part", "audio_only"]
ExportStatus = Literal["pending", "ready", "processing", "completed", "posted"]


# Data models

@dataclass
class VisualBeat:
    """Single visual beat within a scene"""
    id: str
    beatIndex: int
    description: str
    durationSeconds: float
    mediaType: MediaType

    # Production instructions
    productionPrompt: Optional[str] = None

    # Effects
    kenBurns: KenBurnsEffect = KenBurnsEffect.STATIC
    transition: TransitionType = TransitionType.CUT

    # Generated asset (populated by Claude)
    assetUrl: Optional[str] = None


@dataclass
class Scene:
    """Single scene with narration and visual beats"""
    sceneNumber: int
    narratorScript: str
    durationSeconds: float
    visualBeats: List[VisualBeat]

    # Audio assets (populated by Claude)
    audioUrl: Optional[str] = None

    # SFX instructions
    soundEffectDescription: Optional[str] = None
    soundEffectUrl: Optional[str] = None
    sfxTriggerPhrase: Optional[str] = None
    sfxDelay: Optional[float] = None
    sfxVolume: Optional[float] = None


@dataclass
class MasterVolume:
    """Audio mixing levels"""
    voice: float = 1.0
    music: float = 0.3
    sfx: float = 0.6


@dataclass
class GlobalSettings:
    """Global production settings"""
    genre: str
    visualStyle: str
    aspectRatio: str
    masterVolume: MasterVolume
    backgroundAudioUrl: Optional[str] = None


@dataclass
class VideoMetadata:
    """Metadata for video distribution"""
    platform: str
    titles: List[str]
    description: str
    tags: List[str]
    hashtags: List[str]
    thumbnailConcept: str
    strategyTips: List[str]
    rationale: str


@dataclass
class ExportArtifact:
    """Single export job for a platform"""
    id: str
    platform: Platform
    type: ExportType

    # Slicing logic
    startSceneIndex: int
    endSceneIndex: int
    startTime: float
    endTime: float
    duration: float

    # Chunk context
    partNumber: Optional[int] = None
    totalParts: Optional[int] = None

    # Render settings
    renderResolution: RenderResolution = "1080p"
    renderAspectRatio: str = "16:9"
    watermarkText: Optional[str] = None

    # Output (populated by Claude)
    status: ExportStatus = "pending"
    metadata: Optional[VideoMetadata] = None
    downloadUrl: Optional[str] = None


@dataclass
class EngineConfiguration:
    """Engine configuration (for future use)"""
    activeVideoEngineId: str = "ffmpeg-gpu"
    activeTTSEngineId: str = "higgs-audio-v2"
    activeAudioEngineId: str = "musicgen"
    activeImageEngineId: str = "sdxl"
    engineSettings: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    colabUrl: Optional[str] = None
    localBackendUrl: Optional[str] = None


@dataclass
class RenderManifest:
    """
    Complete production manifest from Gemini.

    This is the contract between Gemini (Showrunner) and Claude (Production Engine).
    Gemini writes this to .ai_collaboration/gemini_to_claude/render_manifest.json
    Claude reads, executes, and reports status back.
    """
    projectId: str
    projectTitle: str
    generatedAt: str  # ISO datetime
    globalSettings: GlobalSettings
    scenes: List[Scene]
    exportJobs: List[ExportArtifact]

    # Optional fields
    audioMood: Optional[str] = None
    engineConfig: Optional[EngineConfiguration] = None


@dataclass
class RenderStatus:
    """
    Production status report from Claude to Gemini.

    Claude writes this to .ai_collaboration/claude_to_gemini/RENDER_STATUS.json
    Gemini can poll this to show progress in the UI.
    """
    projectId: str
    status: Literal["IDLE", "PROCESSING", "COMPLETED", "FAILED"]
    progress: float  # 0.0 to 1.0
    currentPhase: str
    estimatedTimeRemaining: Optional[int] = None  # seconds
    exportJobs: List[ExportArtifact] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    lastUpdated: str = field(default_factory=lambda: datetime.now().isoformat())


# Parsing helper
def parse_manifest(data: dict) -> RenderManifest:
    """
    Parse JSON dict into RenderManifest dataclass.

    Args:
        data: JSON dictionary loaded from render_manifest.json

    Returns:
        RenderManifest instance
    """
    # Parse global settings
    global_settings = GlobalSettings(
        genre=data["globalSettings"]["genre"],
        visualStyle=data["globalSettings"]["visualStyle"],
        aspectRatio=data["globalSettings"]["aspectRatio"],
        masterVolume=MasterVolume(**data["globalSettings"]["masterVolume"]),
        backgroundAudioUrl=data["globalSettings"].get("backgroundAudioUrl")
    )

    # Parse scenes
    scenes = []
    for scene_data in data["scenes"]:
        # Parse visual beats
        beats = [
            VisualBeat(
                id=b["id"],
                beatIndex=b["beatIndex"],
                description=b["description"],
                durationSeconds=b["durationSeconds"],
                mediaType=MediaType(b["mediaType"]),
                productionPrompt=b.get("productionPrompt"),
                kenBurns=KenBurnsEffect(b.get("kenBurns", "Static")),
                transition=TransitionType(b.get("transition", "Cut")),
                assetUrl=b.get("assetUrl")
            )
            for b in scene_data["visualBeats"]
        ]

        scene = Scene(
            sceneNumber=scene_data["sceneNumber"],
            narratorScript=scene_data["narratorScript"],
            durationSeconds=scene_data["durationSeconds"],
            visualBeats=beats,
            audioUrl=scene_data.get("audioUrl"),
            soundEffectDescription=scene_data.get("soundEffectDescription"),
            soundEffectUrl=scene_data.get("soundEffectUrl"),
            sfxTriggerPhrase=scene_data.get("sfxTriggerPhrase"),
            sfxDelay=scene_data.get("sfxDelay"),
            sfxVolume=scene_data.get("sfxVolume")
        )
        scenes.append(scene)

    # Parse export jobs
    export_jobs = [
        ExportArtifact(
            id=job["id"],
            platform=job["platform"],
            type=job["type"],
            startSceneIndex=job["startSceneIndex"],
            endSceneIndex=job["endSceneIndex"],
            startTime=job["startTime"],
            endTime=job["endTime"],
            duration=job["duration"],
            partNumber=job.get("partNumber"),
            totalParts=job.get("totalParts"),
            renderResolution=job.get("renderResolution", "1080p"),
            renderAspectRatio=job.get("renderAspectRatio", "16:9"),
            watermarkText=job.get("watermarkText"),
            status=job.get("status", "pending")
        )
        for job in data["exportJobs"]
    ]

    # Parse engine config if present
    engine_config = None
    if "engineConfig" in data:
        engine_config = EngineConfiguration(**data["engineConfig"])

    return RenderManifest(
        projectId=data["projectId"],
        projectTitle=data["projectTitle"],
        generatedAt=data["generatedAt"],
        globalSettings=global_settings,
        scenes=scenes,
        exportJobs=export_jobs,
        audioMood=data.get("audioMood"),
        engineConfig=engine_config
    )
