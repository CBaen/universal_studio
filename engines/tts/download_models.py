"""
Download Piper voice models from HuggingFace
Uses chunked downloading with retry logic for large files
"""

import requests
from pathlib import Path
import time

# Model configuration
MODELS_DIR = Path(__file__).parent / "models"
MODELS_DIR.mkdir(exist_ok=True)

VOICES = [
    {
        "name": "en_US-lessac-medium",
        "path": "en/en_US/lessac/medium",
        "description": "Neutral, professional male voice"
    },
    {
        "name": "en_US-amy-medium",
        "path": "en/en_US/amy/medium",
        "description": "Warm, friendly female voice"
    },
    {
        "name": "en_US-ryan-medium",
        "path": "en/en_US/ryan/medium",
        "description": "Clear, professional male voice"
    }
]

BASE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main"

def download_file(url: str, output_path: Path, max_retries: int = 3):
    """Download file with retry logic and progress tracking"""

    for attempt in range(max_retries):
        try:
            print(f"  Downloading {output_path.name}...")
            print(f"  URL: {url}")
            print(f"  Attempt {attempt + 1}/{max_retries}")

            # Stream download with timeout
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()

            # Get total file size
            total_size = int(response.headers.get('content-length', 0))
            print(f"  File size: {total_size / 1024 / 1024:.2f} MB")

            # Download in chunks
            chunk_size = 8192
            downloaded = 0

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        # Progress indicator every 10MB
                        if downloaded % (10 * 1024 * 1024) < chunk_size:
                            progress = (downloaded / total_size * 100) if total_size > 0 else 0
                            print(f"    Progress: {progress:.1f}% ({downloaded / 1024 / 1024:.1f} MB)")

            # Verify file size
            actual_size = output_path.stat().st_size
            if total_size > 0 and actual_size != total_size:
                raise ValueError(f"Downloaded file size mismatch: {actual_size} != {total_size}")

            print(f"  [OK] Downloaded successfully: {output_path.name}")
            return True

        except Exception as e:
            print(f"  [FAIL] Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                print(f"  Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                print(f"  [FAIL] Failed after {max_retries} attempts")
                return False

def main():
    print("="*60)
    print("PIPER VOICE MODEL DOWNLOADER")
    print("="*60)
    print()

    for voice in VOICES:
        print(f"\nDownloading: {voice['name']}")
        print(f"Description: {voice['description']}")
        print()

        # Download .onnx model
        onnx_url = f"{BASE_URL}/{voice['path']}/{voice['name']}.onnx"
        onnx_path = MODELS_DIR / f"{voice['name']}.onnx"

        if onnx_path.exists():
            print(f"  [SKIP] {onnx_path.name} already exists")
        else:
            if not download_file(onnx_url, onnx_path):
                print(f"  [ERROR] Skipping {voice['name']} due to download failure")
                continue

        # Download .json config
        json_url = f"{BASE_URL}/{voice['path']}/{voice['name']}.onnx.json"
        json_path = MODELS_DIR / f"{voice['name']}.onnx.json"

        if json_path.exists():
            print(f"  [SKIP] {json_path.name} already exists")
        else:
            download_file(json_url, json_path)

    print()
    print("="*60)
    print("DOWNLOAD COMPLETE")
    print("="*60)
    print()
    print(f"Models saved to: {MODELS_DIR.absolute()}")
    print()

    # List downloaded models
    models = list(MODELS_DIR.glob("*.onnx"))
    if models:
        print(f"Downloaded {len(models)} voice models:")
        for model in sorted(models):
            size_mb = model.stat().st_size / 1024 / 1024
            print(f"  [OK] {model.name} ({size_mb:.1f} MB)")
    else:
        print("[WARN] No models downloaded successfully")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Try manually downloading from:")
        print("   https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US")
        print("3. Ensure 'pip install requests' is installed")

if __name__ == "__main__":
    main()
