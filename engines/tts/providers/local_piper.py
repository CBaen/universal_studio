"""
Piper TTS Provider (Tier 1) - Local CPU Execution

Purpose: Fast prototyping engine for rapid iteration
Speed: <1s per scene (fastest in tier system)
Quality: 72/100 (acceptable for prototyping, not final production)
Hardware: CPU-friendly, no GPU required

Use Cases:
- Script testing and iteration
- Rapid prototyping of 9-hour content
- Offline development
- Fallback when remote tiers unavailable
"""

from pathlib import Path
from piper.voice import PiperVoice
from .base import AudioProvider, AudioGenerationRequest, AudioGenerationResult
import wave
import time
import hashlib

class PiperProvider(AudioProvider):
    """
    Tier 1: Fast prototyping engine using Piper TTS

    Configuration:
        voice: Voice model name (e.g., "en_US-lessac-medium")
        models_dir: Directory containing .onnx model files (default: ../models/)
        cache_dir: Directory for caching generated audio (default: ../cache/piper/)

    Example:
        provider = PiperProvider({
            "voice": "en_US-lessac-medium",
            "models_dir": "models/"
        })

        request = AudioGenerationRequest(
            text="Testing Piper TTS",
            voice_id="lessac"
        )

        result = provider.generate(request)
        print(f"Audio: {result.audio_path}")
        print(f"Speed: {result.generation_time_seconds:.2f}s")
    """

    def __init__(self, config: dict):
        super().__init__(config)

        # Voice configuration
        self.voice_model = config.get("voice", "en_US-lessac-medium")

        # Path configuration
        if "models_dir" in config:
            self.models_dir = Path(config["models_dir"])
        else:
            self.models_dir = Path(__file__).parent.parent / "models"

        if "cache_dir" in config:
            self.cache_dir = Path(config["cache_dir"])
        else:
            self.cache_dir = Path(__file__).parent.parent / "cache" / "piper"

        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Model paths
        self.model_path = self.models_dir / f"{self.voice_model}.onnx"
        self.config_path = self.models_dir / f"{self.voice_model}.json"

        # Voice instance (loaded on first use or during warmup)
        self.voice = None

    def warmup(self):
        """
        Preload model into memory

        This should be called once at startup to avoid loading delay
        on first synthesis request. Loads the ONNX model and prepares
        the inference session.
        """
        if not self.is_available():
            raise FileNotFoundError(
                f"Voice model not found: {self.model_path}\n"
                f"Config file: {self.config_path}\n"
                f"Download from: https://huggingface.co/rhasspy/piper-voices"
            )

        print(f"Loading Piper voice: {self.voice_model}")
        start_time = time.time()

        self.voice = PiperVoice.load(str(self.model_path))

        load_time = time.time() - start_time
        print(f"[OK] Piper loaded in {load_time:.2f}s (SR: {self.voice.config.sample_rate}Hz)")

    def generate(self, request: AudioGenerationRequest) -> AudioGenerationResult:
        """
        Generate speech using Piper

        Process:
        1. Check cache for existing audio (hash-based)
        2. If cached, return immediately
        3. If not cached, load model (if needed) and synthesize
        4. Save to cache
        5. Return result with metrics
        """

        # Generate cache key from request
        cache_key = request.to_cache_key()
        output_path = self.cache_dir / f"{cache_key}.wav"

        # Check cache
        if output_path.exists():
            # Return cached result
            with wave.open(str(output_path), "rb") as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                duration = frames / float(rate)

            return AudioGenerationResult(
                audio_path=output_path,
                duration_seconds=duration,
                sample_rate=rate,
                was_cached=True,
                generation_time_seconds=0.0,
                provider_name="Piper",
                quality_score=0.72  # 72/100 baseline
            )

        # Load model if not loaded
        if not self.voice:
            self.warmup()

        # Generate audio
        start_time = time.time()

        with wave.open(str(output_path), "wb") as wav_file:
            # Configure WAV file
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.voice.config.sample_rate)

            # Synthesize text to audio chunks
            for audio_chunk in self.voice.synthesize(request.text):
                wav_file.writeframes(audio_chunk.audio_int16_bytes)

        gen_time = time.time() - start_time

        # Get audio duration
        with wave.open(str(output_path), "rb") as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)

        # Calculate real-time factor (for logging)
        rtf = gen_time / duration if duration > 0 else 0

        print(f"  [Piper] Generated {duration:.2f}s audio in {gen_time:.2f}s (RTF: {rtf:.2f}x)")

        return AudioGenerationResult(
            audio_path=output_path,
            duration_seconds=duration,
            sample_rate=rate,
            was_cached=False,
            generation_time_seconds=gen_time,
            provider_name="Piper",
            quality_score=0.72  # 72/100 baseline
        )

    def is_available(self) -> bool:
        """
        Check if voice model files exist

        Returns:
            True if both .onnx model and .json config exist
        """
        return self.model_path.exists() and self.config_path.exists()

    def supports_voice_cloning(self) -> bool:
        """Piper uses pre-trained voices only (no cloning)"""
        return False

    def supports_emotion_control(self) -> bool:
        """Piper has limited emotion control"""
        return False

    def get_available_voices(self) -> list:
        """
        List all available voice models in the models directory

        Returns:
            List of voice model names (without .onnx extension)
        """
        voices = []
        for onnx_file in self.models_dir.glob("*.onnx"):
            # Check if corresponding .json exists
            json_file = onnx_file.with_suffix(".json")
            if json_file.exists():
                voices.append(onnx_file.stem)

        return sorted(voices)
