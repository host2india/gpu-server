#📌 6. engine/lipsync_engine.py (FP16 CUDA Optimized Wav2Lip)
import torch
import subprocess
from .utils import run_cmd

class LipSyncEngine:
    def __init__(self):
        self.device = "cuda"
        self.fp16 = True

    def sync(self, video, audio, output):
        cmd = (
            f"python3 Wav2Lip/inference.py "
            f"--checkpoint Wav2Lip.pth "
            f"--face '{video}' "
            f"--audio '{audio}' "
            f"--outfile '{output}' "
            f"--fp16"
        )

        out, err = run_cmd(cmd)
        return output
