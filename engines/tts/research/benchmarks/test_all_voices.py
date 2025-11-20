"""
Test all available Piper voices for comparison
"""

import time
import wave
from pathlib import Path
from piper.voice import PiperVoice

# Configuration
OUTPUT_DIR = Path(__file__).resolve().parent / "audio_samples"
OUTPUT_DIR.mkdir(exist_ok=True)

MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"

# Test text (neutral narrative scene)
TEST_TEXT = "In a world where true crime narratives captivate millions, one story stands above the rest. The investigation began with a single anonymous tip."

# Available voices
VOICES = [
    {"name": "en_US-lessac-medium", "description": "Neutral, professional male"},
    {"name": "en_US-amy-medium", "description": "Warm, friendly female"},
    {"name": "en_US-ryan-medium", "description": "Clear, professional male"}
]

def test_voice(voice_name: str, description: str):
    """Test a single voice"""

    print(f"\nTesting: {voice_name}")
    print(f"Description: {description}")

    try:
        # Load voice
        model_path = MODELS_DIR / f"{voice_name}.onnx"

        if not model_path.exists():
            print(f"  [SKIP] Model not found")
            return None

        start_load = time.time()
        voice = PiperVoice.load(str(model_path))
        load_time = time.time() - start_load

        print(f"  Load time: {load_time:.2f}s")
        print(f"  Sample rate: {voice.config.sample_rate}Hz")

        # Generate audio
        output_path = OUTPUT_DIR / f"voice_comparison_{voice_name}.wav"

        start_gen = time.time()

        with wave.open(str(output_path), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(voice.config.sample_rate)

            for audio_chunk in voice.synthesize(TEST_TEXT):
                wav_file.writeframes(audio_chunk.audio_int16_bytes)

        gen_time = time.time() - start_gen

        # Get audio duration
        with wave.open(str(output_path), "rb") as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)

        rtf = gen_time / duration if duration > 0 else 0

        print(f"  Generation time: {gen_time:.2f}s")
        print(f"  Audio duration: {duration:.2f}s")
        print(f"  Real-time factor: {rtf:.2f}x")
        print(f"  [OK] Saved to: {output_path.name}")

        return {
            "name": voice_name,
            "description": description,
            "load_time": load_time,
            "gen_time": gen_time,
            "duration": duration,
            "rtf": rtf
        }

    except Exception as e:
        print(f"  [ERROR] {e}")
        return None

def main():
    print("="*60)
    print("PIPER VOICE COMPARISON TEST")
    print("="*60)
    print(f"\nTest text: \"{TEST_TEXT}\"")
    print(f"Length: {len(TEST_TEXT)} characters\n")

    results = []

    for voice in VOICES:
        result = test_voice(voice["name"], voice["description"])
        if result:
            results.append(result)

    # Summary
    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60 + "\n")

    if results:
        print(f"{'Voice':<25} {'Description':<25} {'Gen Time':<10} {'RTF':<8} {'Duration':<8}")
        print("-" * 80)

        for r in results:
            print(f"{r['name']:<25} {r['description']:<25} {r['gen_time']:<10.2f} {r['rtf']:<8.2f} {r['duration']:<8.2f}")

        print("\nRecommendation:")
        fastest = min(results, key=lambda x: x['rtf'])
        print(f"  Fastest: {fastest['name']} (RTF: {fastest['rtf']:.2f}x)")

        print(f"\nAll samples saved to: {OUTPUT_DIR}")
        print("\nListen to samples to compare voice quality and choose your preferred voice.")

    else:
        print("[WARN] No voices tested successfully")

if __name__ == "__main__":
    main()
