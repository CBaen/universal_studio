"""
Test PiperProvider implementation

Tests:
1. Provider initialization
2. Voice availability check
3. Audio generation
4. Caching behavior
5. Multiple voice support
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from providers.local_piper import PiperProvider
from providers.base import AudioGenerationRequest

def test_piper_provider():
    """Test PiperProvider with different voices"""

    print("="*60)
    print("PIPER PROVIDER TEST")
    print("="*60)

    # Test scenes
    test_scenes = [
        "In a world where true crime narratives captivate millions.",
        "The investigation began on a cold November morning.",
        "But nothing could have prepared them for what they found."
    ]

    # Test with different voices
    voices_to_test = ["en_US-lessac-medium", "en_US-amy-medium", "en_US-ryan-medium"]

    for voice in voices_to_test:
        print(f"\n{'='*60}")
        print(f"Testing voice: {voice}")
        print(f"{'='*60}\n")

        try:
            # Initialize provider
            provider = PiperProvider({"voice": voice})

            # Check availability
            if not provider.is_available():
                print(f"  [SKIP] Voice not found: {voice}")
                print(f"     Download from: https://huggingface.co/rhasspy/piper-voices")
                continue

            print(f"[OK] Voice available: {voice}")

            # Test warmup
            print("\nWarming up...")
            provider.warmup()

            # Test generation with each scene
            for i, text in enumerate(test_scenes, 1):
                print(f"\nScene {i}: \"{text[:50]}...\"")

                request = AudioGenerationRequest(
                    text=text,
                    voice_id=voice
                )

                # First generation (should not be cached)
                result = provider.generate(request)

                print(f"  Generated: {result.audio_path.name}")
                print(f"  Duration: {result.duration_seconds:.2f}s")
                print(f"  Generation time: {result.generation_time_seconds:.2f}s")

                # Calculate RTF
                if result.duration_seconds > 0 and not result.was_cached:
                    rtf = result.generation_time_seconds / result.duration_seconds
                    print(f"  RTF: {rtf:.2f}x")

                print(f"  Cached: {result.was_cached}")
                print(f"  Quality score: {result.quality_score}")

                # Second generation (should be cached)
                result2 = provider.generate(request)
                print(f"  Second call cached: {result2.was_cached}")

                assert result2.was_cached == True, "Second generation should be cached"
                assert result.audio_path == result2.audio_path, "Cached path should match"

        except FileNotFoundError as e:
            print(f"  [ERROR] {e}")
        except Exception as e:
            print(f"  [ERROR] {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

    # Test voice listing
    print(f"\n{'='*60}")
    print("AVAILABLE VOICES")
    print(f"{'='*60}\n")

    provider = PiperProvider({})  # Use defaults
    available_voices = provider.get_available_voices()

    if available_voices:
        print(f"Found {len(available_voices)} voices:")
        for voice in available_voices:
            print(f"  - {voice}")
    else:
        print("[WARN] No voices found")

    print(f"\n{'='*60}")
    print("TEST COMPLETE")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    test_piper_provider()
