#📌 2. app.py (FastAPI + CUDA FP16 server)
from fastapi import FastAPI, UploadFile, File
from engine.lipsync_engine import LipSyncEngine
import os

app = FastAPI()
engine = LipSyncEngine()

@app.post("/api/lipsync")
async def lipsync(audio: UploadFile = File(...), video: UploadFile = File(...)):
    audio_path = f"uploads/{audio.filename}"
    video_path = f"uploads/{video.filename}"
    output_path = f"uploads/output.mp4"

    with open(audio_path, "wb") as f:
        f.write(await audio.read())

    with open(video_path, "wb") as f:
        f.write(await video.read())

    result = engine.sync(video_path, audio_path, output_path)
    return {"status": "success", "output": output_path}
