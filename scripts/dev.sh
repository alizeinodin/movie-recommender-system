#!/usr/bin/env sh
# Print commands to run the full stack (3 terminals). Does not start services.
# Usage: ./scripts/dev.sh   or   sh scripts/dev.sh

set -e
cd "$(dirname "$0")/.."
ROOT="$(pwd)"

echo "Run these in separate terminals from the project root: $ROOT"
echo ""
echo "--- Terminal 1: Backend (Laravel) ---"
echo "  cd $ROOT/backend && php artisan serve --port=8001"
echo ""
echo "--- Terminal 2: ML API (FastAPI) ---"
echo "  cd $ROOT && source venv/bin/activate && uvicorn ml-api.main:app --reload --port 8000"
echo "  (Ensure ml-api/models/ncf_model.pth exists: python ml-api/cli.py train)"
echo ""
echo "--- Terminal 3: Frontend (Nuxt) ---"
echo "  cd $ROOT/frontend && npm run dev"
echo ""
echo "Then open http://localhost:3000"
echo "API: http://127.0.0.1:8001/api/v1  |  ML docs: http://127.0.0.1:8000/docs"
