"""
engine package initializer.

Exports:
- generate_lipsync(...)    -> main entry for lipsync generation
- detect_faces(...)        -> face detection helper
- utils                   -> helper utilities (if needed)

Adjust the imported names if your module functions are named differently.
"""

from __future__ import annotations

import logging

# Package version — update per release if desired
__version__ = "0.1.0"

# Configure simple logger for the engine package
logger = logging.getLogger("gpu_server.engine")
if not logger.handlers:
    # basic configuration (apps can override with their logging config)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[engine] %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Lazy imports of engine components (avoid heavy imports at package import time)
# If your module/function names differ, update these imports.
try:
    from .lipsync_engine import generate_lipsync  # main generate function
except Exception as e:  # pragma: no cover - import-time fallback
    logger.debug("Could not import generate_lipsync: %s", e)
    generate_lipsync = None

try:
    from .face_detector import detect_faces  # face detection helper
except Exception as e:  # pragma: no cover
    logger.debug("Could not import detect_faces: %s", e)
    detect_faces = None

# also expose utils module if present
try:
    from . import utils  # noqa: F401
except Exception:
    utils = None  # pragma: no cover

__all__ = [
    "generate_lipsync",
    "detect_faces",
    "utils",
    "logger",
    "__version__",
]
#If your function names are different (e.g., run_lipsync, lipsync, face_detect), tell me the exact names and I’ll update the file to match.
