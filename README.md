# gpu-server (CPU ONLY)

CPU-safe Wav2Lip server for basic droplets & development.

### Run

pip install -r requirements.txt
python3 models/download_models.py
uvicorn app:app --host 0.0.0.0 --port 8000
