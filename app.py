#Create gpu-server/app.py — FastAPI server and endpoints.
# app.py
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from pathlib import Path
import shutil
import uuid
import asyncio

from engine.lipsync_engine import Wav2LipEngine
from models.download_models import ensure_models_exist

# Setup base folders
BASE_DIR = Path(__file__).resolve().parent
UPLOADS = BASE_DIR / "uploads"
STATIC = BASE_DIR / "static"
UPLOADS.mkdir(exist_ok=True)
STATIC.mkdir(exist_ok=True)

# Load models (downloads if missing)
ensure_models_exist()

# Instantiate engine (detects GPU if available)
engine = Wav2LipEngine()

app = FastAPI(title="gpu-server (hybrid) - Wav2Lip API")

# CORS (allow local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "engine": engine.status()}

@app.get("/models")
async def models_info():
    return {"models": engine.models_info()}

@app.post("/api/lip2sync")
async def lip2sync(background_tasks: BackgroundTasks, audio: UploadFile = File(...), video: UploadFile = File(...)):
    """
    Upload audio + video/image. This forwards to the Wav2Lip engine (sync).
    Returns: { "output": "<relative-path-or-url>" }
    """
    # save uploads
    job_id = str(uuid.uuid4())
    job_dir = UPLOADS / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    audio_path = job_dir / f"audio_{audio.filename}"
    video_path = job_dir / f"video_{video.filename}"

    # Save files to disk
    with audio_path.open("wb") as f:
        shutil.copyfileobj(audio.file, f)
    with video_path.open("wb") as f:
        shutil.copyfileobj(video.file, f)

    # Start job in background to avoid blocking long inference (optional)
    # For synchronous demo we will run inline; easier for testing.
    try:
        # run synchronous processing (blocking) — you can change to background_tasks.add_task(...)
        out_path = await asyncio.get_event_loop().run_in_executor(
            None, lambda: engine.run_sync(str(audio_path), str(video_path), job_dir=str(job_dir))
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Provide accessible URL (static file served via /static/ route)
    if out_path is None:
        raise HTTPException(status_code=500, detail="Engine did not produce output")

    # move/copy to static for download convenience
    out_name = Path(out_path).name
    dest = STATIC / out_name
    shutil.copy(out_path, dest)

    # Return full path (client should use backend host + /static/<file>)
    return {"output": f"/static/{out_name}", "job_id": job_id}

@app.get("/static/{file_name}")
async def static_file(file_name: str):
    f = STATIC / file_name
    if not f.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(f), media_type="video/mp4", filename=file_name)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
