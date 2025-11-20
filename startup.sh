#11) File: startup.sh
#Convenience script to run locally.
#!/usr/bin/env bash
python -m pip install -r requirements.txt
python -c "from models.download_models import ensure_models_exist; ensure_models_exist()"
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
#Make it executable: chmod +x startup.sh
