"""
Download Piper voice models from HuggingFace using official hub library
This method has built-in resume capability and better handling of large files
"""

from huggingface_hub import hf_hub_download
from pathlib import Path
import shutil

# Model configuration
MODELS_DIR = Path(__file__).parent / "models"
MODELS_DIR.mkdir(exist_ok=True)

REPO_ID = "rhasspy/piper-voices"

VOICES = [
    {
        "name": "en_US-lessac-medium",
        "files": [
            "en/en_US/lessac/medium/en_US-lessac-medium.onnx",
            "en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
        ],
        "description": "Neutral, professional male voice"
    },
    {
        "name": "en_US-amy-medium",
        "files": [
            "en/en_US/amy/medium/en_US-amy-medium.onnx",
            "en/en_US/amy/medium/en_US-amy-medium.onnx.json"
        ],
        "description": "Warm, friendly female voice"
    },
    {
        "name": "en_US-ryan-medium",
        "files": [
            "en/en_US/ryan/medium/en_US-ryan-medium.onnx",
            "en/en_US/ryan/medium/en_US-ryan-medium.onnx.json"
        ],
        "description": "Clear, professional male voice"
    }
]

def download_voice(voice_config: dict):
    """Download a voice model using HuggingFace Hub"""

    print(f"\nDownloading: {voice_config['name']}")
    print(f"Description: {voice_config['description']}")

    for file_path in voice_config['files']:
        filename = Path(file_path).name
        output_path = MODELS_DIR / filename

        # Check if already exists
        if output_path.exists():
            size_mb = output_path.stat().st_size / 1024 / 1024
            print(f"  [SKIP] {filename} already exists ({size_mb:.1f} MB)")
            continue

        print(f"  Downloading {filename}...")

        try:
            # Download to HF cache, then copy to our models dir
            downloaded_path = hf_hub_download(
                repo_id=REPO_ID,
                filename=file_path,
                repo_type="model",
                resume_download=True
            )

            # Copy from cache to models dir
            shutil.copy2(downloaded_path, output_path)

            size_mb = output_path.stat().st_size / 1024 / 1024
            print(f"  [OK] {filename} ({size_mb:.1f} MB)")

        except Exception as e:
            print(f"  [FAIL] {filename}: {e}")
            return False

    return True

def main():
    print("="*60)
    print("PIPER VOICE MODEL DOWNLOADER (HuggingFace Hub)")
    print("="*60)

    success_count = 0
    fail_count = 0

    for voice in VOICES:
        if download_voice(voice):
            success_count += 1
        else:
            fail_count += 1

    print()
    print("="*60)
    print("DOWNLOAD COMPLETE")
    print("="*60)
    print()
    print(f"Successfully downloaded: {success_count}/{len(VOICES)} voices")
    print(f"Failed: {fail_count}/{len(VOICES)} voices")
    print()
    print(f"Models saved to: {MODELS_DIR.absolute()}")
    print()

    # List all models
    models = sorted(MODELS_DIR.glob("*.onnx"))
    if models:
        print(f"Available voice models:")
        for model in models:
            size_mb = model.stat().st_size / 1024 / 1024
            print(f"  - {model.stem} ({size_mb:.1f} MB)")
    else:
        print("[WARN] No voice models found")
        print("\nYou can manually download from:")
        print("  https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US")

if __name__ == "__main__":
    main()
