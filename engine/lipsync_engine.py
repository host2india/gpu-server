import subprocess
import os

class LipSyncEngine:
    def __init__(self, device="cpu"):
        self.device = device

    def run(self, image, audio, output):
        cmd = [
            "python3", "Wav2Lip/inference.py",
            "--checkpoint_path", "Wav2Lip/checkpoints/wav2lip_gan.pth",
            "--face", image,
            "--audio", audio,
            "--outfile", output,
            "--device", "cpu"
        ]
        subprocess.run(cmd)
        return output
