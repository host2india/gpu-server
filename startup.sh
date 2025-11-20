#!/bin/bash
python3 models/download_models.py
uvicorn app:app --host 0.0.0.0 --port 8000
