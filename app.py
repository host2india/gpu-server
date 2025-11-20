from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from engine.lipsync_engine import LipSyncEngine

app = FastAPI(title="Wav2Lip CPU Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = LipSyncEngine(device="cpu")

@app.post("/api/lip2sync")
async def lip2sync(audio: UploadFile = File(...), image: UploadFile = File(...)):
    audio_path = f"uploads/{audio.filename}"
    image_path = f"uploads/{image.filename}"
    output_path = f"uploads/output.mp4"

    with open(audio_path, "wb") as f:
        f.write(await audio.read())

    with open(image_path, "wb") as f:
        f.write(await image.read())

    final_video = engine.run(image_path, audio_path, output_path)
    return {"output": final_video}

@app.get("/")
def home():
    return {"status": "cpu-server running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
