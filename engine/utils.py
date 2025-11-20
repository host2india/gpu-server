#6) File: engine/utils.py
#Helper utilities (duration, safe filename).
# engine/utils.py
import os
from pathlib import Path
import re

def safe_filename(name: str) -> str:
    # remove unsafe characters
    return re.sub(r'[^a-zA-Z0-9._-]', '_', name)

def ensure_dir(p: str):
    Path(p).mkdir(parents=True, exist_ok=True)
