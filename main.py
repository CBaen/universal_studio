"""
Production Director - Main Orchestrator

Watches for RenderManifest from Gemini and executes production using all engines.
This is the bridge between Gemini's UI (Showrunner) and Claude's production engines.

Architecture:
    Gemini (UI) → render_manifest.json → Director → Engines → Final Video
                                                    ↓
                                            RENDER_STATUS.json → Gemini (progress updates)
"""

import json
import time
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

from manifest_types import (
    RenderManifest,
    RenderStatus,
    RenderJobStatus,
    ExportArtifact,
    Scene,
    VisualBeat,
    MediaType,
    parse_manifest
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProductionDirector:
    """
    Main orchestrator that executes RenderManifests from Gemini.

    Responsibilities:
    - Watch for new render_manifest.json files
    - Parse and validate manifests
    - Orchestrate all production engines (TTS, Image, Music, SFX, Video)
    - Report progress back to Gemini
    - Handle errors gracefully
    """

    def __init__(self):
        """Initialize Director and locate engines."""
        self.root = Path(__file__).parent
        self.manifest_path = self.root / ".ai_collaboration" / "gemini_to_claude" / "render_manifest.json"
        self.status_path = self.root / ".ai_collaboration" / "claude_to_gemini" / "RENDER_STATUS.json"
        self.output_dir = self.root / "output"
        self.output_dir.mkdir(exist_ok=True)

        # Current project state
        self.current_manifest: Optional[RenderManifest] = None
        self.current_status: Optional[RenderStatus] = None

        # Engine placeholders (will be initialized when engines are ready)
        self.tts_engine = None
        self.image_engine = None
        self.music_engine = None
        self.sfx_engine = None
        self.video_engine = None

        logger.info("ProductionDirector initialized")
        logger.info(f"Watching: {self.manifest_path}")
        logger.info(f"Status output: {self.status_path}")

    def load_engines(self):
        """
        Load production engines.

        NOTE: For now, this is a placeholder. Engines will be imported and
        initialized here once the implementations are ready.
        """
        logger.info("Loading production engines...")

        # TODO: Import and initialize engines
        # from engines.tts.providers.colab_higgs import HiggsAudioProvider
        # from engines.image.providers.local_sdxl import SDXLProvider
        # from engines.music.providers.local_musicgen import MusicGenProvider
        # from engines.sfx.providers.local_audioldm import AudioLDMProvider
        # from engines.video.providers.ffmpeg_gpu import FFmpegGPUProvider

        # self.tts_engine = HiggsAudioProvider(config)
        # self.image_engine = SDXLProvider(config)
        # self.music_engine = MusicGenProvider(config)
        # self.sfx_engine = AudioLDMProvider(config)
        # self.video_engine = FFmpegGPUProvider(config)

        logger.info("Engines loaded (placeholder - will be implemented)")

    def watch_for_manifest(self, poll_interval: float = 2.0):
        """
        Poll for new render_manifest.json files and execute them.

        Args:
            poll_interval: Seconds between checks
        """
        logger.info(f"Starting manifest watcher (poll interval: {poll_interval}s)")

        last_modified = None

        while True:
            try:
                if self.manifest_path.exists():
                    current_modified = self.manifest_path.stat().st_mtime

                    # Check if file was modified since last check
                    if last_modified is None or current_modified > last_modified:
                        logger.info("New manifest detected!")
                        last_modified = current_modified

                        # Load and execute
                        manifest = self.load_manifest()
                        if manifest:
                            self.execute_manifest(manifest)

                time.sleep(poll_interval)

            except KeyboardInterrupt:
                logger.info("Watcher stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in watcher loop: {e}", exc_info=True)
                time.sleep(poll_interval)

    def load_manifest(self) -> Optional[RenderManifest]:
        """
        Load and parse render_manifest.json.

        Returns:
            RenderManifest instance or None if parsing failed
        """
        try:
            logger.info(f"Loading manifest from {self.manifest_path}")

            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            manifest = parse_manifest(data)
            logger.info(f"Manifest loaded: {manifest.projectTitle} ({manifest.projectId})")
            logger.info(f"  Scenes: {len(manifest.scenes)}")
            logger.info(f"  Export jobs: {len(manifest.exportJobs)}")

            self.current_manifest = manifest
            return manifest

        except Exception as e:
            logger.error(f"Failed to load manifest: {e}", exc_info=True)
            self.update_status(
                project_id="unknown",
                status="FAILED",
                progress=0.0,
                phase="Failed to load manifest",
                estimated_time_remaining=0,
                errors=[str(e)]
            )
            return None

    def execute_manifest(self, manifest: RenderManifest):
        """
        Execute complete production pipeline for a manifest.

        Pipeline:
        1. Generate all TTS audio (narration)
        2. Generate all images/videos (visual beats)
        3. Generate background music
        4. Generate sound effects
        5. Assemble final videos (one per export job)
        6. Report completion

        Args:
            manifest: The production manifest from Gemini
        """
        logger.info(f"Starting production for: {manifest.projectTitle}")
        start_time = time.time()

        try:
            # Initialize status
            # Calculate rough time estimate based on scene count
            total_scenes = len(manifest.scenes)
            total_beats = sum(len(scene.visualBeats) for scene in manifest.scenes)
            estimated_time = (total_scenes * 30) + (total_beats * 45)  # Rough estimate

            self.update_status(
                project_id=manifest.projectId,
                status="PROCESSING",
                progress=0.0,
                phase="Starting production...",
                estimated_time_remaining=estimated_time
            )

            # Phase 1: Generate TTS audio
            self.phase_generate_tts(manifest)

            # Phase 2: Generate visuals
            self.phase_generate_visuals(manifest)

            # Phase 3: Generate background music
            self.phase_generate_music(manifest)

            # Phase 4: Generate sound effects
            self.phase_generate_sfx(manifest)

            # Phase 5: Assemble videos
            self.phase_assemble_videos(manifest)

            # Mark complete
            elapsed = time.time() - start_time
            logger.info(f"Production complete in {elapsed:.1f}s")

            # Convert ExportArtifact objects to RenderJobStatus for status reporting
            job_statuses = [
                RenderJobStatus(
                    id=job.id,
                    platform=job.platform,
                    status=job.status,
                    downloadUrl=job.downloadUrl,
                    error=None
                )
                for job in manifest.exportJobs
            ]

            self.update_status(
                project_id=manifest.projectId,
                status="COMPLETED",
                progress=1.0,
                phase=f"Production complete ({elapsed:.1f}s)",
                estimated_time_remaining=0,
                export_jobs=job_statuses
            )

        except Exception as e:
            logger.error(f"Production failed: {e}", exc_info=True)
            self.update_status(
                project_id=manifest.projectId,
                status="FAILED",
                progress=0.0,
                phase="Production failed",
                estimated_time_remaining=0,
                errors=[str(e)]
            )

    def estimate_time_remaining(self, progress: float, start_time: float, total_scenes: int, total_beats: int) -> int:
        """Estimate remaining time based on current progress."""
        if progress == 0:
            # Initial estimate
            return (total_scenes * 30) + (total_beats * 45)

        elapsed = time.time() - start_time
        if progress > 0:
            total_estimated = elapsed / progress
            remaining = total_estimated - elapsed
            return max(0, int(remaining))
        return 0

    def phase_generate_tts(self, manifest: RenderManifest):
        """Phase 1: Generate TTS audio for all scenes."""
        logger.info("PHASE 1: Generating TTS audio...")
        total_scenes = len(manifest.scenes)
        phase_start = time.time()

        for idx, scene in enumerate(manifest.scenes):
            logger.info(f"  Generating audio for scene {scene.sceneNumber}/{total_scenes}")
            logger.info(f"    Script: {scene.narratorScript[:80]}...")

            # Update progress
            progress = (idx / total_scenes) * 0.25  # TTS is 25% of total
            total_beats = sum(len(s.visualBeats) for s in manifest.scenes)
            estimated_time = self.estimate_time_remaining(progress, phase_start, total_scenes, total_beats)

            self.update_status(
                project_id=manifest.projectId,
                status="PROCESSING",
                progress=progress,
                phase=f"Generating scene {scene.sceneNumber}/{total_scenes} audio",
                estimated_time_remaining=estimated_time
            )

            # TODO: Generate TTS audio
            # result = self.tts_engine.generate(AudioGenerationRequest(
            #     text=scene.narratorScript,
            #     voice_persona=manifest.voicePersona,
            #     duration=scene.durationSeconds
            # ))
            # scene.audioUrl = str(result.audio_path)

            # Placeholder: Mock audio generation
            scene.audioUrl = f"output/audio/scene_{scene.sceneNumber:03d}.wav"
            logger.info(f"    ✓ Audio: {scene.audioUrl}")

        logger.info("PHASE 1 complete: All TTS audio generated")

    def phase_generate_visuals(self, manifest: RenderManifest):
        """Phase 2: Generate images/videos for all visual beats."""
        logger.info("PHASE 2: Generating visuals...")

        total_beats = sum(len(scene.visualBeats) for scene in manifest.scenes)
        total_scenes = len(manifest.scenes)
        beat_count = 0
        phase_start = time.time()

        for scene in manifest.scenes:
            for beat in scene.visualBeats:
                beat_count += 1
                logger.info(f"  Generating visual {beat_count}/{total_beats}")
                logger.info(f"    Prompt: {beat.productionPrompt[:80]}...")

                # Update progress
                progress = 0.25 + (beat_count / total_beats) * 0.35  # Visuals are 35% of total
                estimated_time = self.estimate_time_remaining(progress, phase_start, total_scenes, total_beats)

                self.update_status(
                    project_id=manifest.projectId,
                    status="PROCESSING",
                    progress=progress,
                    phase=f"Generating visual {beat_count}/{total_beats}",
                    estimated_time_remaining=estimated_time
                )

                # TODO: Generate image/video based on mediaType
                # if beat.mediaType == MediaType.IMAGE:
                #     result = self.image_engine.generate(ImageGenerationRequest(
                #         prompt=beat.productionPrompt,
                #         style=manifest.globalSettings.visualStyle,
                #         aspect_ratio=manifest.globalSettings.aspectRatio
                #     ))
                #     beat.assetUrl = str(result.image_path)

                # Placeholder: Mock image generation
                beat.assetUrl = f"output/images/scene_{scene.sceneNumber:03d}_beat_{beat.beatIndex:02d}.png"
                logger.info(f"    ✓ Visual: {beat.assetUrl}")

        logger.info("PHASE 2 complete: All visuals generated")

    def phase_generate_music(self, manifest: RenderManifest):
        """Phase 3: Generate background music."""
        logger.info("PHASE 3: Generating background music...")

        if manifest.globalSettings.backgroundAudioUrl:
            logger.info("  Background music already provided, skipping generation")
            return

        if not manifest.audioMood:
            logger.info("  No audioMood specified, skipping music generation")
            return

        phase_start = time.time()
        total_scenes = len(manifest.scenes)
        total_beats = sum(len(s.visualBeats) for s in manifest.scenes)
        estimated_time = self.estimate_time_remaining(0.60, phase_start, total_scenes, total_beats)

        self.update_status(
            project_id=manifest.projectId,
            status="PROCESSING",
            progress=0.60,
            phase="Generating background music",
            estimated_time_remaining=estimated_time
        )

        logger.info(f"  Mood: {manifest.audioMood}")

        # TODO: Generate music
        # total_duration = sum(scene.durationSeconds for scene in manifest.scenes)
        # result = self.music_engine.generate(MusicGenerationRequest(
        #     prompt=f"Documentary background music, {manifest.audioMood}",
        #     duration=total_duration,
        #     mood=manifest.audioMood
        # ))
        # manifest.globalSettings.backgroundAudioUrl = str(result.audio_path)

        # Placeholder: Mock music generation
        manifest.globalSettings.backgroundAudioUrl = "output/music/background_music.mp3"
        logger.info(f"  ✓ Music: {manifest.globalSettings.backgroundAudioUrl}")

        logger.info("PHASE 3 complete: Background music generated")

    def phase_generate_sfx(self, manifest: RenderManifest):
        """Phase 4: Generate sound effects for scenes."""
        logger.info("PHASE 4: Generating sound effects...")

        sfx_scenes = [s for s in manifest.scenes if s.soundEffectDescription]
        if not sfx_scenes:
            logger.info("  No SFX requested, skipping")
            return

        phase_start = time.time()
        total_scenes = len(manifest.scenes)
        total_beats = sum(len(s.visualBeats) for s in manifest.scenes)

        for idx, scene in enumerate(sfx_scenes):
            logger.info(f"  Generating SFX for scene {scene.sceneNumber}")
            logger.info(f"    Description: {scene.soundEffectDescription}")

            progress = 0.70 + (idx / len(sfx_scenes)) * 0.10  # SFX is 10% of total
            estimated_time = self.estimate_time_remaining(progress, phase_start, total_scenes, total_beats)

            self.update_status(
                project_id=manifest.projectId,
                status="PROCESSING",
                progress=progress,
                phase=f"Generating SFX {idx + 1}/{len(sfx_scenes)}",
                estimated_time_remaining=estimated_time
            )

            # TODO: Generate SFX
            # result = self.sfx_engine.generate(SFXGenerationRequest(
            #     prompt=scene.soundEffectDescription,
            #     duration=5.0,  # SFX are typically short
            #     volume=scene.sfxVolume or 0.6
            # ))
            # scene.soundEffectUrl = str(result.audio_path)

            # Placeholder: Mock SFX generation
            scene.soundEffectUrl = f"output/sfx/scene_{scene.sceneNumber:03d}_sfx.wav"
            logger.info(f"    ✓ SFX: {scene.soundEffectUrl}")

        logger.info("PHASE 4 complete: All SFX generated")

    def phase_assemble_videos(self, manifest: RenderManifest):
        """Phase 5: Assemble final videos for each export job."""
        logger.info("PHASE 5: Assembling videos...")

        phase_start = time.time()
        total_scenes = len(manifest.scenes)
        total_beats = sum(len(s.visualBeats) for s in manifest.scenes)

        for idx, job in enumerate(manifest.exportJobs):
            logger.info(f"  Assembling export job {idx + 1}/{len(manifest.exportJobs)}")
            logger.info(f"    Platform: {job.platform}")
            logger.info(f"    Resolution: {job.renderResolution} {job.renderAspectRatio}")

            progress = 0.80 + (idx / len(manifest.exportJobs)) * 0.20  # Assembly is 20% of total
            estimated_time = self.estimate_time_remaining(progress, phase_start, total_scenes, total_beats)

            self.update_status(
                project_id=manifest.projectId,
                status="PROCESSING",
                progress=progress,
                phase=f"Assembling {job.platform} video {idx + 1}/{len(manifest.exportJobs)}",
                estimated_time_remaining=estimated_time
            )

            # TODO: Assemble video
            # scenes_slice = manifest.scenes[job.startSceneIndex:job.endSceneIndex + 1]
            # result = self.video_engine.assemble(VideoAssemblyRequest(
            #     scenes=scenes_slice,
            #     resolution=job.renderResolution,
            #     aspect_ratio=job.renderAspectRatio,
            #     background_music=manifest.globalSettings.backgroundAudioUrl,
            #     master_volume=manifest.globalSettings.masterVolume,
            #     watermark=job.watermarkText
            # ))
            # job.downloadUrl = str(result.video_path)
            # job.status = "completed"

            # Placeholder: Mock video assembly
            filename = f"{manifest.projectId}_{job.platform}_{job.renderAspectRatio.replace(':', 'x')}.mp4"
            job.downloadUrl = f"output/videos/{filename}"
            job.status = "completed"
            logger.info(f"    ✓ Video: {job.downloadUrl}")

        logger.info("PHASE 5 complete: All videos assembled")

    def update_status(
        self,
        project_id: str,
        status: str,
        progress: float,
        phase: str,
        estimated_time_remaining: int = 0,
        export_jobs: list = None,
        errors: list = None
    ):
        """
        Update production status and write to RENDER_STATUS.json.

        Args:
            project_id: Project ID
            status: IDLE, PROCESSING, COMPLETED, FAILED
            progress: 0.0 to 1.0
            phase: Current phase description
            estimated_time_remaining: Estimated seconds remaining (required)
            export_jobs: List of RenderJobStatus objects (for completion)
            errors: List of error messages
        """
        self.current_status = RenderStatus(
            projectId=project_id,
            status=status,
            progress=progress,
            currentPhase=phase,
            estimatedTimeRemaining=estimated_time_remaining,
            exportJobs=export_jobs or [],
            errors=errors or []
        )

        # Write to file for Gemini to read
        try:
            status_data = {
                "projectId": self.current_status.projectId,
                "status": self.current_status.status,
                "progress": self.current_status.progress,
                "currentPhase": self.current_status.currentPhase,
                "estimatedTimeRemaining": self.current_status.estimatedTimeRemaining,
                "exportJobs": [
                    {
                        "id": job.id,
                        "platform": job.platform,
                        "status": job.status,
                        "downloadUrl": job.downloadUrl,
                        "error": job.error
                    }
                    for job in self.current_status.exportJobs
                ],
                "errors": self.current_status.errors,
                "lastUpdated": self.current_status.lastUpdated
            }

            with open(self.status_path, 'w', encoding='utf-8') as f:
                json.dump(status_data, f, indent=2)

            logger.debug(f"Status updated: {status} - {phase} ({progress:.1%})")

        except Exception as e:
            logger.error(f"Failed to write status: {e}")

    def run_once(self):
        """Execute a single manifest (for testing)."""
        if self.manifest_path.exists():
            manifest = self.load_manifest()
            if manifest:
                self.execute_manifest(manifest)
        else:
            logger.warning(f"No manifest found at {self.manifest_path}")


def main():
    """Main entry point."""
    import sys

    director = ProductionDirector()

    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        # Run once for testing
        logger.info("Running in single-execution mode")
        director.run_once()
    else:
        # Watch mode
        logger.info("Running in watch mode (Ctrl+C to stop)")
        director.watch_for_manifest()


if __name__ == "__main__":
    main()
