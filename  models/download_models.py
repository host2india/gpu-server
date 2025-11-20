import gdown
import os

os.makedirs("models", exist_ok=True)

print("Downloading FP16 model...")
gdown.download(
    "https://drive.google.com/uc?id=1oQrGuje3ewSdyuicuaGWuxh-yLCo5RNC",
    "models/Wav2Lip.pth",
    quiet=False,
)
