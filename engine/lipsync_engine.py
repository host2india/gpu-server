#4) File: engine/lipsync_engine.py
#This file contains a wrapper that auto-detects GPU and runs a simplified Wav2Lip invocation. It's written to be easy to integrate with a real Wav2Lip script; currently it includes a safe mock fallback if you don't have the model yet.
# engine/lipsync_engine.py
import os
import subprocess
from pathlib import Path
import time
import shutil
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
DEFAULT_OUTPUT_DIR = BASE_DIR / "static"

class Wav2LipEngine:
    def __init__(self):
        # detect cuda availability (simple)
        self.cuda = self._detect_cuda()
        self.wav2lip_checkpoint = MODELS_DIR / "wav2lip_gan.pth"
        self.s3fd_checkpoint = MODELS_DIR / "s3fd.pth"
        self._loaded = self.wav2lip_checkpoint.exists()
        self._info = {
            "cuda": self.cuda,
            "wav2lip_exists": self.wav2lip_checkpoint.exists(),
            "s3fd_exists": self.s3fd_checkpoint.exists(),
        }

    def _detect_cuda(self):
        try:
            import torch
            return torch.cuda.is_available()
        except Exception:
            return False

    def status(self):
        return {
            "cuda": self.cuda,
            "ready": self._loaded
        }

    def models_info(self):
        return self._info

    def run_sync(self, audio_path: str, video_path: str, job_dir: str = None) -> str:
        """
        Run the Wav2Lip pipeline. This is a synchronous call that returns path to output file.
        If actual Wav2Lip isn't installed / checkpoint missing, we return a mock sample video path.
        """

        audio_path = str(audio_path)
        video_path = str(video_path)
        out_name = f"out_{int(time.time())}.mp4"
        out_path = (Path(job_dir) if job_dir else Path(DEFAULT_OUTPUT_DIR)) / out_name

        # If Wav2Lip model available -> call real script
        if self._loaded:
            # NOTE: expected that Wav2Lip repo is present and has the inference script.
            # You may adapt command to your local installation.
            wav2lip_repo = BASE_DIR / "Wav2Lip"  # optional place to clone the repo
            if wav2lip_repo.exists():
                # Example command (adjust as needed)
                cmd = [
                    sys.executable,
                    str(wav2lip_repo / "inference" / "infer.py"),
                    "--checkpoint_path", str(self.wav2lip_checkpoint),
                    "--face", video_path,
                    "--audio", audio_path,
                    "--outfile", str(out_path),
                ]
                # Use GPU flag if CUDA available
                if self.cuda:
                    cmd += ["--face_det_batch_size", "16", "--resize_factor", "1"]
                else:
                    cmd += ["--face_det_batch_size", "8"]

                print("Running Wav2Lip:", " ".join(cmd))
                subprocess.check_call(cmd)
                return str(out_path)
            else:
                # fallback: call a lightweight local script (not provided) — for now return mock
                print("Wav2Lip repo not present at", wav2lip_repo, "- returning mock output")
        else:
            print("Wav2Lip checkpoint not found. Returning mock output video")

        # Mock behavior: if there's a sample in static named sample-output.mp4, copy it
        sample = BASE_DIR / "static" / "sample-output.mp4"
        if sample.exists():
            shutil.copy(sample, out_path)
            return str(out_path)

        # Create a tiny silent MP4 if ffmpeg available (1-second) as a safe fallback
        try:
            subprocess.check_call([
                "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=white:s=640x480:d=1", "-f", "lavfi", "-i", "anullsrc",
                "-shortest", "-c:v", "libx264", "-c:a", "aac", "-strict", "-2", str(out_path)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return str(out_path)
        except Exception:
            # Last resort: return None
            return None
