# Full-Stack Movie Recommender – Setup & Run

This project has four parts:

1. **ML model** (Python) – NCF model and training
2. **ML API** (FastAPI) – Serves recommendations from the trained model
3. **Backend** (Laravel) – REST API for movies, ratings, and recommendations (calls ML API)
4. **Frontend** (Nuxt) – Netflix-style UI to browse movies and rate them

---

## Prerequisites

- PHP 8.2+ (Laravel)
- Composer
- Node.js 18+ (Nuxt)
- Python 3.10+ with venv (ML)

---

## 1. Backend (Laravel)

```bash
cd backend
cp .env.example .env   # if not already
php artisan key:generate
# Use SQLite (default) or set DB_* in .env
php artisan migrate
php artisan db:seed --class=MovieLensSeeder
php artisan serve --port=8001
```

**Movie posters:** The seeder fetches poster URLs from the [FM-DB (Free Movie DB) API](https://imdb.iamidiotareyoutoo.com/docs/index.html). No API key is required. After seeding movies and ratings, it calls the API for each title and saves `#IMG_POSTER` to `movies.poster_url`. To use a different base URL, set `FMDB_API_URL` in `.env`.

API base: **http://127.0.0.1:8001**  
API v1 base: **http://127.0.0.1:8001/api/v1**  
Routes: `/api/v1/movies`, `/api/v1/ratings`, `/api/v1/recommendations/{userId}`

---

## 2. ML API (FastAPI) – for recommendations

All ML code, data, and the trained model live inside **ml-api/**.

Train the model first (from project root):

```bash
source venv/bin/activate
pip install -r ml-api/requirements.txt
python ml-api/cli.py train   # creates ml-api/models/ncf_model.pth
```

Then start the ML API (from **project root**):

```bash
source venv/bin/activate
cd ml-api && uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Laravel calls **http://127.0.0.1:8000/recommend?user_id={id}&top_k=10** (same as `python ml-api/cli.py demo`).  
If the ML API is not running, the backend returns a deterministic fallback and does **not** cache it, so the next request will try the ML API again.

**If the frontend shows different movies than `python ml-api/cli.py demo`** (e.g. for user 196), ensure the ML API uses the same logic (it does: sorted movie order), then clear caches and refresh:
1. **ML API in-memory cache:** restart the ML API, or call `POST http://127.0.0.1:8000/recommend/clear-cache`
2. **Laravel cache:** `cd backend && php artisan recommendations:clear-cache`
3. Reload the frontend; recommendations will match the demo.

**Check that the ML API runs and Laravel can connect (any user 1–943):**
```bash
# From project root
python scripts/check_ml_api.py
# Or custom URL:
python scripts/check_ml_api.py http://127.0.0.1:8000
```
The script verifies `/health`, `/ready` (model loaded), `/recommend` for user 1 and last user, and that invalid `user_id` returns 400.

---

## 3. Frontend (Nuxt)

```bash
cd frontend
npm install
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8001/api npm run dev
```

Open **http://localhost:3000**.  
You can change the “User” dropdown to see different recommendation lists (MovieLens user IDs 1–943).

---

## 4. Summary – run order for presentation

1. **Terminal 1 – Laravel**
   ```bash
   cd backend && php artisan serve --port=8001
   ```

2. **Terminal 2 – ML API**
   ```bash
   source venv/bin/activate && cd ml-api && uvicorn main:app --reload --port 8000
   ```
   (Ensure `ml-api/models/ncf_model.pth` exists: run `python ml-api/cli.py train` once.)

3. **Terminal 3 – Nuxt**
   ```bash
   cd frontend && npm run dev
   ```

4. Open **http://localhost:3000** in the browser.

---

## Environment

- **Backend (.env)**  
  - `ML_API_URL=http://127.0.0.1:8000` (optional; default is this).

- **Frontend**  
  - `NUXT_PUBLIC_API_BASE=http://127.0.0.1:8001/api/v1` (optional; default is this).

- **CORS**  
  - Laravel `config/cors.php` allows `localhost:3000` and `127.0.0.1:3000`.
