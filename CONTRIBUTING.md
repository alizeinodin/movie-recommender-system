# Contributing to Movie Recommender System

Thanks for your interest in improving this project. This document explains how to set up the repo and contribute.

---

## Development setup

1. **Clone and install**
   - Backend: `cd backend && cp .env.example .env && composer install && php artisan key:generate && php artisan migrate && php artisan db:seed --class=MovieLensSeeder`
   - Frontend: `cd frontend && npm install`
   - ML: from project root, `python -m venv venv && source venv/bin/activate` (or `venv\Scripts\activate` on Windows), then `pip install -r ml-api/requirements.txt` and `python ml-api/cli.py train` once

2. **Run the stack**  
   See [SETUP.md](SETUP.md) for the run order (Laravel on 8001, ML API on 8000, Nuxt on 3000). You can use `./scripts/dev.sh` from the project root to print commands for each terminal.

3. **API**
   - Backend API is versioned: base URL is `/api/v1` (e.g. `http://127.0.0.1:8001/api/v1/movies`).
   - ML API docs: `http://127.0.0.1:8000/docs` when the service is running.

---

## Code style and practices

- **Backend (Laravel):** Use PSR-12; API responses via Resources; validation in FormRequest or `$request->validate()`; return unified error shape (`message`, `code`, `errors` when applicable).
- **Frontend (Nuxt):** Use TypeScript where helpful; follow existing patterns (composables, components); ensure accessibility (labels, focus styles).
- **ML (Python):** Follow existing structure in `ml-api/src`; keep inference deterministic and documented in OpenAPI.

---

## Pull requests

1. Create a branch from `main` (e.g. `feature/your-feature` or `fix/your-fix`).
2. Make your changes and ensure the app still runs (backend, ML API, frontend).
3. If you add new API routes or env vars, update README or SETUP and `.env.example`.
4. Open a PR with a short description of the change and reference any issue.

---

## Reporting issues

Include: what you did, what you expected, what happened, and your environment (OS, PHP/Node/Python versions). For API errors, include the request URL and response body if possible.
