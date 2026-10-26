#!/usr/bin/env python3
"""
Run the ML API from project root (fixes "No module named 'ml-api'" when IDE or
command uses project root as cwd). Spawns uvicorn with cwd=ml-api so that
"main:app" resolves correctly.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ML_API_DIR = ROOT / "ml-api"
if not ML_API_DIR.is_dir():
    print("Error: ml-api directory not found.", file=sys.stderr)
    sys.exit(1)

sys.exit(
    subprocess.run(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--reload",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
        ],
        cwd=str(ML_API_DIR),
    ).returncode
)
