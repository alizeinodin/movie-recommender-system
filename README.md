# Movie Recommender System

Full-stack **deep learning** movie recommender: NCF model (MovieLens 100K), FastAPI ML service, Laravel backend, Nuxt frontend.

---

## Quick start

1. **Backend:** `cd backend && cp .env.example .env && php artisan key:generate && php artisan migrate && php artisan db:seed --class=MovieLensSeeder && php artisan serve --port=8001`
2. **ML (train once):** `source venv/bin/activate && pip install -r ml-api/requirements.txt && python ml-api/cli.py train` (from project root)
3. **ML API:** `source venv/bin/activate && cd ml-api && uvicorn main:app --reload --port 8000` (from project root)
4. **Frontend:** `cd frontend && npm install && npm run dev`
5. Open **http://localhost:3000**

Or run `./scripts/dev.sh` to print the commands for each terminal. See **[SETUP.md](SETUP.md)** for details and **[CONTRIBUTING.md](CONTRIBUTING.md)** for development workflow.

---

## Project structure

| Part        | Role |
|------------|------|
| **ml-api/**| All ML: FastAPI service, `src/` (model, train, evaluate, demo), `data/`, `models/`, `cli.py` (train/evaluate/demo) |
| **backend/** | Laravel API (v1): movies, ratings, recommendations (calls ML API) |
| **frontend/** | Nuxt app: browse movies, rate, see recommendations |
| **scripts/** | Utilities (`check_ml_api.py`, `dev.sh`) |

Recommendations in the frontend match **`python ml-api/cli.py demo`** (e.g. user 196) when the ML API is running and caches are cleared after changes (see SETUP.md).

---

## Environment variables

| Variable | Used by | Description |
|----------|--------|-------------|
| `ML_API_URL` | Backend | ML API base URL (default: `http://127.0.0.1:8000`) |
| `FMDB_API_URL` | Backend | Optional. FM-DB API base URL for poster URLs (default: `https://imdb.iamidiotareyoutoo.com`). The seeder uses [FM-DB](https://imdb.iamidiotareyoutoo.com/docs/index.html) to fetch movie posters; no API key required. |
| `NUXT_PUBLIC_API_BASE` | Frontend | Laravel API base URL (default: `http://127.0.0.1:8001/api/v1`) |

Backend uses `backend/.env`; copy from `backend/.env.example`. Root `.env.example` lists all services for reference.
