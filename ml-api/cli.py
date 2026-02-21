#!/usr/bin/env python3
"""
CLI for the ML recommender: train, evaluate, demo.
Run from ml-api directory: python cli.py [train|evaluate|demo]
Or from project root: python ml-api/cli.py [train|evaluate|demo]

Activate venv first: source venv/bin/activate (from project root).
"""
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data" / "ml-100k"
MODEL_DIR = PROJECT_ROOT / "models"

# So that src imports work from ml-api
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

try:
    import torch  # noqa: F401
except ModuleNotFoundError:
    print("Error: PyTorch is not installed. Activate the project virtual environment first:")
    print("  source venv/bin/activate   # from project root")
    print("  pip install -r ml-api/requirements.txt")
    sys.exit(1)


def run_train():
    """Run training."""
    os.chdir(PROJECT_ROOT)
    from train import train
    train(data_dir=str(DATA_DIR), model_dir=str(MODEL_DIR))


def run_evaluate():
    """Run evaluation."""
    os.chdir(PROJECT_ROOT)
    from evaluate import evaluate
    model_path = MODEL_DIR / "ncf_model.pth"
    if not model_path.exists():
        print(f"Model not found at {model_path}. Run 'python cli.py train' first.")
        sys.exit(1)
    evaluate(model_path=str(model_path), data_dir=str(DATA_DIR))


def run_demo():
    """Run demo recommendations."""
    os.chdir(PROJECT_ROOT)
    from demo import main as demo_main
    demo_main()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cli.py [train|evaluate|demo]")
        print("  train    - Train the NCF model")
        print("  evaluate - Evaluate on test set")
        print("  demo     - Get movie recommendations for a sample user")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "train":
        run_train()
    elif cmd == "evaluate":
        run_evaluate()
    elif cmd == "demo":
        run_demo()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
