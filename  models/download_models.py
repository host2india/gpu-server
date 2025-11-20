#7) File: models/download_models.py
#Downloads model files from Google Drive links you provided earlier. This uses gdown (easy for drive). It will not commit the big checkpoint to git — it downloads at runtime.
# models/download_models.py
#Important: the WAV2LIP_DRIVE and S3FD_DRIVE values are set to the direct-download patterns for the Google Drive IDs you posted earlier. If your links are different or gated, replace them or ensure the files are accessible.
import os
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# === CHANGE THESE to your drive IDs / links (user provided earlier) ===
# Example share links you gave earlier:
WAV2LIP_DRIVE = "https://drive.google.com/uc?id=1oQrGuje3ewSdyuicuaGWuxh-yLCo5RNC"   # wav2lip_gan.pth
S3FD_DRIVE   = "https://drive.google.com/uc?id=1BbJGJHpXp0aqEMnvMCBMlv7neEbVcbV1"   # s3fd.pth

# target filenames
WAV2LIP_FILE = MODELS_DIR / "wav2lip_gan.pth"
S3FD_FILE = MODELS_DIR / "s3fd.pth"

def _call(cmd):
    print(">", " ".join(cmd))
    subprocess.check_call(cmd)

def download_with_gdown(url, dest: Path):
    try:
        import gdown
    except Exception:
        print("gdown not installed; attempting to pip install it.")
        _call([sys.executable, "-m", "pip", "install", "gdown"])
        import gdown

    if dest.exists():
        print(f"{dest} already exists — skipping download.")
        return
    print(f"Downloading {url} -> {dest} ...")
    gdown.download(url, str(dest), quiet=False)

def ensure_models_exist():
    """
    Ensure required checkpoints exist. If not, attempt to download using gdown.
    """
    if not WAV2LIP_FILE.exists():
        print("wav2lip checkpoint missing. Attempting download...")
        download_with_gdown(WAV2LIP_DRIVE, WAV2LIP_FILE)
    else:
        print("wav2lip checkpoint already present:", WAV2LIP_FILE)

    if not S3FD_FILE.exists():
        print("s3fd checkpoint missing. Attempting download...")
        download_with_gdown(S3FD_DRIVE, S3FD_FILE)
    else:
        print("s3fd checkpoint already present:", S3FD_FILE)

if __name__ == "__main__":
    ensure_models_exist()
