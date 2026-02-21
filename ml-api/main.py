"""
FastAPI service that exposes the NCF model for movie recommendations.
Best practices: deterministic inference, in-memory cache per user, eval mode.

Run from project root: uvicorn ml-api.main:app --reload --host 0.0.0.0 --port 8000
Or from ml-api directory: uvicorn main:app --reload --port 8000
"""
import sys
from pathlib import Path

# ml-api directory is the project root for this service (model, data, src live here)
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import time
import logging

import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ml-api")

# Lazy load model (single load, eval mode)
_model = None
_mappings = None

# In-memory cache: (user_id, top_k) -> {"movie_ids": [...], "scores": [...]}
_recommend_cache: dict[tuple[int, int], dict] = {}

# Similar-movies cache: (movie_id, top_k) -> {"movie_ids": [...], "scores": [...]}
_similar_cache: dict[tuple[int, int], dict] = {}

# Precomputed item embeddings for fast similar-movie lookups (lazy)
_item_embeddings = None


def get_item_embeddings():
    """Lazy precompute all item embeddings for similar-movie endpoint (performance)."""
    global _item_embeddings
    if _item_embeddings is None:
        from utils import get_all_item_embeddings
        model, mappings = get_model()
        _item_embeddings = get_all_item_embeddings(
            model, mappings["movie2idx"], device=torch.device("cpu")
        )
    return _item_embeddings


def get_model():
    global _model, _mappings
    if _model is None:
        from model import NCF
        from prepareData import load_data

        checkpoint_path = PROJECT_ROOT / "models" / "ncf_model.pth"
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Model not found: {checkpoint_path}")

        checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
        _model = NCF(
            num_users=checkpoint["num_users"],
            num_items=checkpoint["num_movies"],
            embedding_dim=checkpoint.get("embedding_dim", 32),
        )
        _model.load_state_dict(checkpoint["model_state_dict"])
        _model.eval()

        data_dir = str(PROJECT_ROOT / "data" / "ml-100k")
        (_, _, _, _, _, _, user2idx, movie2idx, idx2user, idx2movie, movie_names) = load_data(data_dir=data_dir)
        _mappings = {
            "user2idx": user2idx,
            "movie2idx": movie2idx,
            "idx2movie": idx2movie,
            "movie_names": movie_names,
        }
    return _model, _mappings


APP_VERSION = "1.0.0"

app = FastAPI(
    title="ML Recommender API",
    version=APP_VERSION,
    description="NCF-based movie recommendations for MovieLens 100K. Used by the Laravel backend.",
    docs_url="/docs",
    redoc_url="/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log request method, path, and duration for observability."""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info("%s %s %d %.1fms", request.method, request.url.path, response.status_code, duration_ms)
        return response


app.add_middleware(RequestLoggingMiddleware)


@app.get("/version", tags=["Meta"])
def version():
    """API and model version for debugging and deployment checks."""
    try:
        model, mappings = get_model()
        return {
            "api_version": APP_VERSION,
            "model_loaded": True,
            "num_users": len(mappings["user2idx"]),
            "num_items": len(mappings["movie2idx"]),
        }
    except FileNotFoundError:
        return {"api_version": APP_VERSION, "model_loaded": False}
    except Exception:
        return {"api_version": APP_VERSION, "model_loaded": False}


@app.get("/health", tags=["Health"])
def health():
    """Liveness: process is up. Use /ready for model readiness."""
    return {"status": "ok"}


@app.post("/recommend/clear-cache")
def clear_recommend_cache():
    """Clear in-memory recommendation and similar-movie caches (e.g. after model/data change)."""
    global _recommend_cache, _similar_cache, _item_embeddings
    _recommend_cache.clear()
    _similar_cache.clear()
    _item_embeddings = None
    return {"status": "ok", "message": "Recommendation and similar-movie caches cleared."}


@app.get("/ready", tags=["Health"])
def ready():
    """Readiness: model loaded and can serve any user (1 to num_users)."""
    try:
        model, mappings = get_model()
        n_users = len(mappings["user2idx"])
        return {
            "status": "ready",
            "model_loaded": True,
            "num_users": n_users,
            "user_id_range": [1, n_users],
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Not ready: {e!s}")


@app.get("/recommend", tags=["Recommendations"])
def recommend(user_id: int, top_k: int = 10):
    """Return top-k recommended movie IDs and scores for the given user (MovieLens user_id 1–943). Deterministic, cached; same logic as `python ml-api/cli.py demo`."""
    cache_key = (user_id, top_k)
    if cache_key in _recommend_cache:
        return _recommend_cache[cache_key]

    try:
        model, mappings = get_model()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    user2idx = mappings["user2idx"]
    if user_id not in user2idx:
        raise HTTPException(status_code=400, detail=f"user_id must be 1-{len(user2idx)} (MovieLens user ID)")

    try:
        from utils import recommend_top_movies

        device = torch.device("cpu")
        recommendations = recommend_top_movies(
            model,
            user_id,
            mappings["user2idx"],
            mappings["movie2idx"],
            mappings["idx2movie"],
            mappings["movie_names"],
            top_k=top_k,
            device=device,
        )
        # Same shape as before: movie_ids and scores; ensure JSON-serializable (e.g. numpy.int64 -> int)
        result = {
            "movie_ids": [int(mid) for mid, _title, pred in recommendations],
            "scores": [float(round(pred, 2)) for _mid, _title, pred in recommendations],
        }
        _recommend_cache[cache_key] = result
        return result
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Recommendation failed: {e!s}")


@app.get("/similar", tags=["Recommendations"])
def similar(movie_id: int, top_k: int = 12):
    """Return top-k movie IDs and similarity scores for movies similar to the given movie (item-based). Cached."""
    cache_key = (movie_id, top_k)
    if cache_key in _similar_cache:
        return _similar_cache[cache_key]

    try:
        model, mappings = get_model()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    movie2idx = mappings["movie2idx"]
    if movie_id not in movie2idx:
        raise HTTPException(
            status_code=400,
            detail=f"movie_id must be a known movie ID (e.g. 1–{max(movie2idx)})",
        )

    try:
        from utils import similar_movies

        device = torch.device("cpu")
        all_emb = get_item_embeddings()
        results = similar_movies(
            model,
            movie_id,
            movie2idx,
            mappings["idx2movie"],
            mappings["movie_names"],
            top_k=top_k,
            exclude_self=True,
            device=device,
            all_embeddings=all_emb,
        )
        result = {
            "movie_ids": [int(mid) for mid, _title, _score in results],
            "scores": [float(score) for _mid, _title, score in results],
        }
        _similar_cache[cache_key] = result
        return result
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Similar movies failed: {e!s}")