# gpu-server (main - hybrid)

Hybrid FastAPI server for Wav2Lip-based lip-sync inference.
Supports CPU-only mode for development and detects GPU at runtime for faster inference.

## Structure
- `app.py` — FastAPI app with `/api/lip2sync` endpoint
- `engine/` — engine wrapper (Wav2Lip runner)
- `models/` — model downloader and storage
- `static/` — outputs served from `/static/<file>`
- `uploads/` — temp uploads (gitignored)

## Quickstart (local CPU)
1. Create a Python venv
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
(Optional) Download models (the script will attempt to download from Drive if missing)

bash
Copy code
python -c "from models.download_models import ensure_models_exist; ensure_models_exist()"
Start server

bash
Copy code
uvicorn app:app --reload --host 0.0.0.0 --port 8000
Test:

Health: GET http://localhost:8000/health

Models: GET http://localhost:8000/models

Lip2Sync (multipart POST): POST http://localhost:8000/api/lip2sync with audio and video files.

Outputs will be returned as /static/<file> URL; server serves them from static/.

GPU notes
To leverage GPU, install the appropriate torch+CUDA wheel for your environment. Example for CUDA 12.6:

bash
Copy code
pip install torch --index-url https://download.pytorch.org/whl/cu126
Confirm GPU with python -c "import torch; print(torch.cuda.is_available())"

Colab
This repo can be used in Colab. Clone, run models/download_models.py or upload checkpoints, then run app.py.


