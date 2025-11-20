# TTS Engine Testing Plan

## Objective
Test 3 TTS engines on local hardware (i7-1260P, 32GB RAM, Intel iGPU) to validate:
1. Installation simplicity
2. Voice selection and tuning capabilities
3. Inference speed (English-only)
4. Audio quality and expressiveness
5. Hardware requirements

---

## Test Matrix

| Engine | Installation | Hardware Target | Expected Speed | Quality Target |
|--------|--------------|----------------|----------------|----------------|
| Piper | `pip install piper-tts` | CPU (i7-1260P) | <1s per scene | 72/100 |
| Chatterbox | `pip install chatterbox-tts` | iGPU/CPU | 2-5s per scene | 89/100 |
| Higgs Audio V2 | Manual setup | Colab (24GB GPU) | 10-20s per scene | 92/100 |

---

## Phase 1: Chatterbox (Priority 1)

### Installation
```bash
pip install chatterbox-tts
```

### Key Features to Test
- [x] **Voice Cloning**: Zero-shot voice cloning from reference audio
- [x] **Emotion Control**: `exaggeration` parameter (0.0-1.0)
- [x] **Pacing Control**: `cfg_weight` parameter (0.0-1.0)
- [x] **Pre-trained Voices**: Test default voice quality
- [x] **Custom Voices**: Load user-provided reference audio

### Test Script
```python
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

# Test 1: Default voice
model = ChatterboxTTS.from_pretrained(device="cpu")  # or "cuda" if available
text = "In a world where true crime narratives captivate millions, one story stands above the rest."
wav = model.generate(text)
ta.save("test_default.wav", wav, model.sr)

# Test 2: Emotion exaggeration
wav_dramatic = model.generate(text, exaggeration=0.8, cfg_weight=0.3)
ta.save("test_dramatic.wav", wav_dramatic, model.sr)

# Test 3: Voice cloning (requires reference audio)
REFERENCE_AUDIO = "path/to/voice_sample.wav"
wav_cloned = model.generate(text, audio_prompt_path=REFERENCE_AUDIO)
ta.save("test_cloned.wav", wav_cloned, model.sr)
```

### Expected Outcomes
- **Installation**: <5 minutes
- **Model Loading**: 30-60 seconds (first run)
- **Generation Speed**: 2-5 seconds per scene (50-100 words)
- **Quality**: Near-ElevenLabs quality (89/100)

### Voice Tuning Parameters

| Parameter | Range | Effect | Use Case |
|-----------|-------|--------|----------|
| `exaggeration` | 0.0 - 1.0 | Emotional intensity | 0.5 = balanced, 0.8 = dramatic |
| `cfg_weight` | 0.0 - 1.0 | Pacing/deliberation | 0.3 = slow/deliberate, 0.5 = natural |
| `temperature` | 0.0 - 1.0 | Randomness (if supported) | 0.7 = creative, 0.3 = consistent |

---

## Phase 2: Piper (Priority 2)

### Installation
```bash
pip install piper-tts
```

### Key Features to Test
- [x] **Speed**: Fastest inference (target <1s per scene)
- [x] **CPU Performance**: No GPU required
- [x] **Voice Selection**: Available English voices
- [x] **Quality**: Acceptable for prototyping (72/100)

### Test Script
```bash
# Command-line test
echo "This is a test of the Piper TTS engine" | piper \
  --model en_US-lessac-medium.onnx \
  --output_file test_piper.wav
```

### Python API Test
```python
from piper import PiperVoice

voice = PiperVoice.load("en_US-lessac-medium")
audio = voice.synthesize("This is a test of the Piper TTS engine")
# Save audio...
```

### Expected Outcomes
- **Installation**: <2 minutes
- **Generation Speed**: <1 second per scene
- **Quality**: Good for rapid prototyping, slightly robotic

---

## Phase 3: Higgs Audio V2 (Priority 3 - Colab Only)

### Installation (Google Colab)
```bash
# In Colab notebook
!git clone https://github.com/boson-ai/higgs-audio.git
%cd higgs-audio
!pip install -r requirements.txt
!pip install -e .
```

### Key Features to Test
- [x] **Voice Cloning**: Zero-shot from reference audio
- [x] **Multi-speaker**: Automatic voice assignment
- [x] **Temperature Control**: Generation randomness
- [x] **Smart Voice Selection**: Automatic voice based on text

### Test Script (Colab)
```python
from boson_multimodal.serve.serve_engine import HiggsAudioServeEngine, HiggsAudioResponse
from boson_multimodal.data_types import ChatMLSample, Message
import torch
import torchaudio

MODEL_PATH = "bosonai/higgs-audio-v2-generation-3B-base"
AUDIO_TOKENIZER_PATH = "bosonai/higgs-audio-v2-tokenizer"

system_prompt = (
    "Generate audio following instruction.\n\n<|scene_desc_start|>\n"
    "Audio is recorded from a quiet room.\n<|scene_desc_end|>"
)

messages = [
    Message(role="system", content=system_prompt),
    Message(role="user", content="In a world where true crime narratives captivate millions, one story stands above the rest."),
]

serve_engine = HiggsAudioServeEngine(MODEL_PATH, AUDIO_TOKENIZER_PATH, device="cuda")

output = serve_engine.generate(
    chat_ml_sample=ChatMLSample(messages=messages),
    max_new_tokens=1024,
    temperature=0.3,
    top_p=0.95,
    stop_strings=["<|end_of_text|>", "<|eot_id|>"],
)

torchaudio.save("test_higgs.wav", torch.from_numpy(output.audio)[None, :], output.sampling_rate)
```

### Expected Outcomes
- **Hardware**: Requires 24GB GPU (Colab Pro/A100)
- **Generation Speed**: 10-20 seconds per scene
- **Quality**: Highest quality (92/100), near-perfect expressiveness

---

## Test Scenes (English Narration)

### Test 1: Neutral Narration
"The investigation began on a cold November morning when Detective Martinez received an anonymous tip."

### Test 2: Dramatic Narration (High Emotion)
"But nothing could have prepared them for what they found behind that door."

### Test 3: Conversational Tone
"You might be wondering, how did they miss such obvious clues? Let me explain."

### Test 4: Long-form Consistency (500+ words)
[Full paragraph to test voice consistency over extended content]

---

## Quality Metrics

### Automated Metrics
- **PESQ Score**: Perceptual Evaluation of Speech Quality (0-4.5)
- **WER**: Word Error Rate (re-transcribe with Whisper, compare to input)
- **Inference Speed**: Real-time factor (audio duration / generation time)

### Manual Evaluation
- **Expressiveness**: 1-10 scale (naturalness, emotion, prosody)
- **Voice Consistency**: Does voice remain stable across multiple scenes?
- **Pronunciation**: Are technical terms pronounced correctly?
- **Background Noise**: Any artifacts, clicks, or robotic sounds?

---

## Testing Status

- [ ] **Chatterbox**: Install and test default voice
- [ ] **Chatterbox**: Test emotion exaggeration (0.3, 0.5, 0.8)
- [ ] **Chatterbox**: Test voice cloning with reference audio
- [ ] **Chatterbox**: Generate 10 test scenes, measure speed
- [ ] **Piper**: Install and test fastest voice
- [ ] **Piper**: Compare quality vs Chatterbox
- [ ] **Higgs Audio V2**: Document Colab setup requirements
- [ ] **Higgs Audio V2**: Test on Colab with 3 reference voices
- [ ] **Quality Comparison**: Generate same scene with all 3 engines
- [ ] **Documentation**: Update findings.md with test results

---

## Next Steps

1. ✅ Install Chatterbox locally
2. ✅ Test on i7-1260P (CPU mode first)
3. ✅ Generate test samples with varying `exaggeration` values
4. ✅ Document voice tuning best practices
5. ✅ Implement ChatterboxProvider in `engines/tts/providers/`
6. ✅ Move to Piper testing (Tier 1)
7. ✅ Create Colab notebook for Higgs Audio V2 testing

---

**Last Updated**: 2025-11-19
**Status**: Phase 1 (Chatterbox) - Ready to Begin Testing
