# Project structure

This document describes the layout of the recommander system and where each concern lives.

---

## Root layout

```
recommanderSystem/
├── README.md              # This repo overview and quick start
├── SETUP.md               # Step-by-step run order and env
├── BEST_PRACTICES.md      # Backend and ML practices
├── PRESENTATION.md        # How to present the demo
├── PROJECT_STRUCTURE.md   # This file
├── venv/                  # Python virtualenv (use for ML API; create from root)
├── ml-api/                # All ML: API, CLI, source, data, model
│   ├── main.py            # FastAPI app (run from ml-api: uvicorn main:app)
│   ├── cli.py             # CLI: train, evaluate, demo
│   ├── requirements.txt   # Python deps for ML
│   ├── src/               # NCF model, train, evaluate, demo, utils, prepareData
│   ├── data/ml-100k/      # MovieLens 100K (u.data, u.item, etc.)
│   └── models/            # Trained model (ncf_model.pth) after cli.py train
├── backend/               # Laravel API
├── frontend/              # Nuxt app
└── scripts/               # Helper scripts (e.g. check_ml_api.py)
```

---

## What runs where

| Component   | Command / entry point        | Port / URL              |
|------------|------------------------------|--------------------------|
| Laravel    | `php artisan serve --port=8001` | http://127.0.0.1:8001   |
| ML API     | `cd ml-api && uvicorn main:app --port 8000` (venv from root) | http://127.0.0.1:8000 |
| Nuxt       | `npm run dev` in frontend    | http://localhost:3000    |

The frontend calls the Laravel API at **/api/v1** (e.g. `/api/v1/movies`, `/api/v1/recommendations/{userId}`). Laravel calls the ML API (`/recommend?user_id=&top_k=10`) for recommendations. All API errors use a unified JSON shape: `{ message, code?, errors? }`.

---

## ML and ML API (aligned with demo)

- **All ML lives in ml-api/:** `ml-api/src/` (model, prepareData, train, evaluate, demo, utils), `ml-api/data/`, `ml-api/models/`, `ml-api/cli.py`, `ml-api/main.py`.
- **CLI:** `python ml-api/cli.py [train|evaluate|demo]` (from project root). Demo uses `recommend_top_movies()` from `src/utils.py` with **sorted movie order** so results are deterministic.
- **ML API:** `ml-api/main.py` uses `PROJECT_ROOT = ml-api directory`, loads `models/ncf_model.pth` and `data/ml-100k`, same sorted iteration as the demo so `/recommend` matches `python ml-api/cli.py demo` (e.g. user 196).
- **Paths:** Run uvicorn from inside **ml-api** (`cd ml-api && uvicorn main:app --reload --port 8000`); model and data paths are relative to the ml-api directory. (Python does not accept module names with a hyphen, so use the ml-api directory as cwd.)

---

## Backend (Laravel)

- **API:** `backend/routes/api.php` → movies, ratings, recommendations.
- **Recommendations:** `RecommendationController` calls the ML API; on success it caches; on failure it returns a deterministic fallback and does **not** cache.
- **Cache clear:** `php artisan recommendations:clear-cache` (see SETUP.md).

---

## Frontend (Nuxt)

- **App:** `frontend/` – pages, components, composables; API base from `NUXT_PUBLIC_API_BASE` (default `http://127.0.0.1:8001/api`).
- **User:** Persisted in localStorage; recommendations are per user (MovieLens user IDs 1–943).

---

## Matching the demo in the UI

For user 196 (and others), the first movie in the frontend should match the first line of `python ml-api/cli.py demo` (e.g. Schindler's List). To ensure that:

1. Use the **same model and logic**: ML API already uses sorted movie order like the demo.
2. **Restart the ML API** after code/model changes, or call **POST /recommend/clear-cache** on the ML API to clear its in-memory cache.
3. Run **`php artisan recommendations:clear-cache`** in the backend so Laravel refetches from the ML API.
4. Reload the frontend.
