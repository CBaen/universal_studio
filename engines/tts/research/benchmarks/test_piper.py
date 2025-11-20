"""
Piper TTS Testing Script
Tests Piper's speed and quality on local hardware
"""

import time
import wave
from pathlib import Path
from piper.voice import PiperVoice

# Test configuration
OUTPUT_DIR = Path(__file__).parent / "audio_samples"
OUTPUT_DIR.mkdir(exist_ok=True)

# Models directory (relative to this script)
# benchmarks/ -> research/ -> tts/ -> models/
MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"

# Test scenes
TEST_SCENES = {
    "neutral": "The investigation began on a cold November morning when Detective Martinez received an anonymous tip.",
    "dramatic": "But nothing could have prepared them for what they found behind that door.",
    "conversational": "You might be wondering, how did they miss such obvious clues? Let me explain.",
    "long_form": """In the world of true crime, some cases stand out not just for their brutality,
    but for the intricate web of lies and deception that surrounds them. Today, we're diving deep
    into a case that has baffled investigators for over a decade. A case where every answer
    led to more questions, and where the truth, when it finally emerged, was far stranger
    than anyone could have imagined."""
}

def test_piper(voice_model="en_US-lessac-medium"):
    """Test Piper TTS with different scenes"""

    print(f"\\n{'='*60}")
    print("PIPER TTS TEST")
    print(f"{'='*60}\\n")

    print(f"Loading voice model: {voice_model}")
    print(f"Models directory: {MODELS_DIR}")

    try:
        # Load voice from models directory
        # Piper expects path WITH .onnx extension for the model file
        # but WITHOUT extension for the config (it adds .json automatically)
        model_path = MODELS_DIR / f"{voice_model}.onnx"
        print(f"Full model path: {model_path}")

        # Check if files exist
        onnx_file = model_path
        json_file = MODELS_DIR / f"{voice_model}.json"
        print(f"ONNX exists: {onnx_file.exists()}")
        print(f"JSON exists: {json_file.exists()}")

        if not onnx_file.exists() or not json_file.exists():
            raise FileNotFoundError(f"Missing model files for {voice_model}")

        voice = PiperVoice.load(str(model_path))
        print(f"[OK] Voice model loaded successfully\\n")

        results = []

        for scene_name, text in TEST_SCENES.items():
            print(f"Testing scene: {scene_name}")
            print(f"Text length: {len(text)} characters")

            # Measure generation time
            start_time = time.time()

            # Generate audio - synthesize returns audio chunks
            output_path = OUTPUT_DIR / f"piper_{scene_name}.wav"

            with wave.open(str(output_path), "wb") as wav_file:
                # Configure WAV file
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(voice.config.sample_rate)

                # Synthesize and write audio chunks
                for audio_chunk in voice.synthesize(text):
                    wav_file.writeframes(audio_chunk.audio_int16_bytes)

            generation_time = time.time() - start_time

            # Get audio duration
            with wave.open(str(OUTPUT_DIR / f"piper_{scene_name}.wav"), "rb") as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                audio_duration = frames / float(rate)

            # Calculate real-time factor
            rtf = generation_time / audio_duration if audio_duration > 0 else 0

            print(f"  Generation time: {generation_time:.2f}s")
            print(f"  Audio duration: {audio_duration:.2f}s")
            print(f"  Real-time factor: {rtf:.2f}x")
            print(f"  Output: {OUTPUT_DIR / f'piper_{scene_name}.wav'}\\n")

            results.append({
                "scene": scene_name,
                "chars": len(text),
                "gen_time": generation_time,
                "audio_dur": audio_duration,
                "rtf": rtf
            })

        # Summary
        print(f"\\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}\\n")

        avg_rtf = sum(r["rtf"] for r in results) / len(results)
        avg_gen_time = sum(r["gen_time"] for r in results) / len(results)

        print(f"Average generation time: {avg_gen_time:.2f}s")
        print(f"Average real-time factor: {avg_rtf:.2f}x")

        if avg_rtf < 0.5:
            speed_rating = "[EXCELLENT] Faster than real-time"
        elif avg_rtf < 1.0:
            speed_rating = "[GOOD] Near real-time"
        else:
            speed_rating = "[SLOW] Slower than real-time"

        print(f"Speed rating: {speed_rating}")
        print(f"\\nAll samples saved to: {OUTPUT_DIR}")

        return results

    except FileNotFoundError as e:
        print(f"\\n[ERROR] FileNotFoundError: {e}")
        print(f"Looked in: {MODELS_DIR}")
        import traceback
        traceback.print_exc()
        return None

    except Exception as e:
        print(f"\\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_piper()
