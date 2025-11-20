# TTS Engine - Quick Start Guide

**Goal**: Get Tier 1 (Piper) working in 10 minutes

---

## Step 1: Download Piper Voice Models (5 min)

### Option A: Direct Download (Recommended)
Visit: https://github.com/rhasspy/piper/releases/tag/2023.11.14-2

**Download these files** to `engines/tts/models/`:

1. **en_US-lessac-medium** (Neutral, professional):
   - `en_US-lessac-medium.onnx` (16.9 MB)
   - `en_US-lessac-medium.onnx.json` (1 KB)

2. **en_US-amy-medium** (Warm, friendly):
   - `en_US-amy-medium.onnx` (16.9 MB)
   - `en_US-amy-medium.onnx.json` (1 KB)

3. **en_GB-alan-medium** (British, authoritative):
   - `en_GB-alan-medium.onnx` (16.9 MB)
   - `en_GB-alan-medium.onnx.json` (1 KB)

### Option B: Command Line (if wget available)
```bash
cd engines/tts/models

# Lessac (neutral)
wget https://github.com/rhasspy/piper/releases/download/2023.11.14-2/en_US-lessac-medium.onnx
wget https://github.com/rhasspy/piper/releases/download/2023.11.14-2/en_US-lessac-medium.onnx.json

# Amy (warm)
wget https://github.com/rhasspy/piper/releases/download/2023.11.14-2/en_US-amy-medium.onnx
wget https://github.com/rhasspy/piper/releases/download/2023.11.14-2/en_US-amy-medium.onnx.json

# Alan (British)
wget https://github.com/rhasspy/piper/releases/download/2023.11.14-2/en_GB-alan-medium.onnx
wget https://github.com/rhasspy/piper/releases/download/2023.11.14-2/en_GB-alan-medium.onnx.json
```

---

## Step 2: Test Piper (2 min)

```bash
cd engines/tts/research/benchmarks
python test_piper.py
```

**Expected Output**:
```
============================================================
PIPER TTS TEST
============================================================

Loading voice model: en_US-lessac-medium
✓ Voice model loaded successfully

Testing scene: neutral
Text length: 92 characters
  Generation time: 0.45s
  Audio duration: 5.2s
  Real-time factor: 0.09x
  Output: benchmarks/audio_samples/piper_neutral.wav

...

============================================================
SUMMARY
============================================================

Average generation time: 0.52s
Average real-time factor: 0.11x
Speed rating: ⚡ EXCELLENT

All samples saved to: benchmarks/audio_samples
```

**Listen to the samples**:
- Open `engines/tts/research/benchmarks/audio_samples/`
- Play `piper_neutral.wav`, `piper_dramatic.wav`, etc.

**Quality check**:
- Is it robotic? (Expected: slightly, but usable)
- Is pronunciation correct?
- Is speed acceptable?

---

## Step 3: Implement PiperProvider (3 min)

Create `engines/tts/providers/local_piper.py`:

```python
from pathlib import Path
from piper.voice import PiperVoice
from .base import AudioProvider, AudioGenerationRequest, AudioGenerationResult
import wave
import time
import hashlib

class PiperProvider(AudioProvider):
    """
    Tier 1: Fast prototyping engine using Piper TTS
    - Speed: <1s per scene (fastest)
    - Quality: 72/100 (acceptable for prototyping)
    - Hardware: CPU-friendly
    """

    def __init__(self, config: dict):
        super().__init__(config)
        model_name = config.get("voice", "en_US-lessac-medium")
        self.model_path = Path(__file__).parent.parent / "models" / f"{model_name}.onnx"
        self.voice = None
        self.cache_dir = Path(__file__).parent.parent / "cache" / "piper"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def warmup(self):
        """Preload model into memory"""
        if not self.is_available():
            raise FileNotFoundError(
                f"Voice model not found: {self.model_path}\\n"
                f"Download from: https://github.com/rhasspy/piper/releases"
            )

        print(f"Loading Piper voice: {self.model_path.stem}")
        self.voice = PiperVoice.load(str(self.model_path.with_suffix('')))
        print(f"✅ Piper loaded (SR: {self.voice.config.sample_rate}Hz)")

    def generate(self, request: AudioGenerationRequest) -> AudioGenerationResult:
        """Generate speech using Piper"""

        # Check cache
        cache_key = request.to_cache_key()
        output_path = self.cache_dir / f"{cache_key}.wav"

        if output_path.exists():
            # Return cached result
            with wave.open(str(output_path), "rb") as wav_file:
                duration = wav_file.getnframes() / wav_file.getframerate()

            return AudioGenerationResult(
                audio_path=output_path,
                duration_seconds=duration,
                sample_rate=22050,
                was_cached=True,
                generation_time_seconds=0.0,
                provider_name="Piper"
            )

        # Load model if not loaded
        if not self.voice:
            self.warmup()

        # Generate
        start_time = time.time()

        with wave.open(str(output_path), "wb") as wav_file:
            wav_file.setparams((1, 2, 22050, 0, 'NONE', 'NONE'))
            self.voice.synthesize(request.text, wav_file)

        gen_time = time.time() - start_time

        # Get duration
        with wave.open(str(output_path), "rb") as wav_file:
            duration = wav_file.getnframes() / wav_file.getframerate()

        return AudioGenerationResult(
            audio_path=output_path,
            duration_seconds=duration,
            sample_rate=22050,
            was_cached=False,
            generation_time_seconds=gen_time,
            provider_name="Piper",
            quality_score=0.72  # 72/100
        )

    def is_available(self) -> bool:
        """Check if voice model exists"""
        return self.model_path.exists() and self.model_path.with_suffix('.onnx.json').exists()

    def supports_voice_cloning(self) -> bool:
        return False  # Piper uses pre-trained voices only

    def supports_emotion_control(self) -> bool:
        return False  # Piper has limited emotion control
```

---

## Step 4: Test PiperProvider

Create `engines/tts/test_provider.py`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from providers.local_piper import PiperProvider
from providers.base import AudioGenerationRequest

# Test with different voices
voices = ["en_US-lessac-medium", "en_US-amy-medium", "en_GB-alan-medium"]

for voice in voices:
    print(f"\\nTesting voice: {voice}")

    try:
        provider = PiperProvider({"voice": voice})

        request = AudioGenerationRequest(
            text="In a world where true crime narratives captivate millions.",
            voice_id=voice
        )

        result = provider.generate(request)

        print(f"  Generated: {result.audio_path.name}")
        print(f"  Duration: {result.duration_seconds:.2f}s")
        print(f"  Generation time: {result.generation_time_seconds:.2f}s")
        print(f"  RTF: {result.generation_time_seconds / result.duration_seconds:.2f}x")
        print(f"  Cached: {result.was_cached}")

    except FileNotFoundError as e:
        print(f"  ⚠️  Voice not found: {voice}")
        print(f"     Download from: https://github.com/rhasspy/piper/releases")
```

**Run**:
```bash
cd engines/tts
python test_provider.py
```

**Expected Output**:
```
Testing voice: en_US-lessac-medium
Loading Piper voice: en_US-lessac-medium
✅ Piper loaded (SR: 22050Hz)
  Generated: a1b2c3d4e5f6.wav
  Duration: 4.20s
  Generation time: 0.38s
  RTF: 0.09x
  Cached: False

Testing voice: en_US-amy-medium
Loading Piper voice: en_US-amy-medium
✅ Piper loaded (SR: 22050Hz)
  Generated: f6e5d4c3b2a1.wav
  Duration: 4.25s
  Generation time: 0.41s
  RTF: 0.10x
  Cached: False
```

---

## Next: Colab Setup (Tier 2 & 3)

1. **Open**: `colab/tts_worker.ipynb` in Google Colab
2. **Run all cells** (installs Chatterbox + Higgs)
3. **Copy ngrok URL** from Cell 7
4. **Test from local machine**:

```python
import requests

WORKER_URL = "https://xxxx.ngrok-free.app"  # From Colab

response = requests.post(f"{WORKER_URL}/generate", json={
    "text": "Testing Chatterbox from local machine",
    "engine": "chatterbox",
    "exaggeration": 0.7
})

with open("colab_test.wav", "wb") as f:
    f.write(response.content)

print("✅ Audio saved from Colab worker")
```

---

## Troubleshooting

### Piper: "FileNotFoundError"
**Problem**: Voice model not downloaded
**Solution**: Download `.onnx` + `.json` files to `engines/tts/models/`

### Piper: "UnicodeEncodeError"
**Problem**: Windows console encoding issue
**Solution**: Run in PowerShell with `chcp 65001` first, or ignore emoji characters

### Colab: "Quota exceeded"
**Problem**: Free tier GPU limit reached
**Solution**: Wait 12 hours or use Colab Pro ($10/month)

### Colab: "Module not found"
**Problem**: Installation failed
**Solution**: Re-run installation cells, check error messages

---

## File Checklist

After completing Quick Start:

- [x] Piper installed (`pip install piper-tts`)
- [ ] 3 voice models downloaded to `engines/tts/models/`
- [ ] `test_piper.py` runs successfully
- [ ] Audio samples generated in `benchmarks/audio_samples/`
- [ ] `local_piper.py` implemented
- [ ] `test_provider.py` runs successfully
- [ ] Colab notebook uploaded and tested
- [ ] ngrok URL obtained from Colab
- [ ] Remote API tested from local machine

---

## Success = Tier 1 Complete

✅ **When Tier 1 is working**:
- Piper generates audio in <1s
- Multiple voices available
- PiperProvider caches results
- Can prototype scripts rapidly

**Next goal**: Get Chatterbox (Tier 2) running on Colab for production quality.

---

**Time estimate**: 10-15 minutes for Tier 1, 30-45 minutes for Tier 2 (Colab)
