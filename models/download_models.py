import gdown
import os

def download_all():

    os.makedirs("Wav2Lip/checkpoints", exist_ok=True)

    print("▶ Downloading wav2lip_gan.pth…")
    gdown.download(
        "https://drive.google.com/uc?id=1oQrGuje3ewSdyuicuaGWuxh-yLCo5RNC",
        "Wav2Lip/checkpoints/wav2lip_gan.pth",
        quiet=False
    )

    print("▶ Downloading s3fd.pth…")
    gdown.download(
        "https://drive.google.com/uc?id=1BbJGJHpXp0aqEMnvMCBMlv7neEbVcbv1",
        "Wav2Lip/face_detection/detection/s3fd.pth",
        quiet=False
    )

    print("✔ Downloads complete")

if __name__ == "__main__":
    download_all()
