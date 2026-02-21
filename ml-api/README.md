# ML Recommender API

All ML code for the movie recommender lives here: NCF model, training, evaluation, demo, and the FastAPI service.

## Layout

- **main.py** – FastAPI app (recommendations, health, ready, clear-cache)
- **cli.py** – CLI: `train`, `evaluate`, `demo`
- **src/** – model, prepareData, train, evaluate, demo, utils
- **data/ml-100k/** – MovieLens 100K dataset
- **models/** – Trained model (`ncf_model.pth`) after training
- **requirements.txt** – Python dependencies

## Commands (from project root)

```bash
source venv/bin/activate
pip install -r ml-api/requirements.txt

# Train (creates ml-api/models/ncf_model.pth)
python ml-api/cli.py train

# Evaluate
python ml-api/cli.py evaluate

# Demo (top-10 for user 196)
python ml-api/cli.py demo

# Start the API (for Laravel/frontend)
uvicorn ml-api.main:app --reload --port 8000
```

From **ml-api** directory you can also run: `python cli.py train`, `uvicorn main:app --port 8000`.
