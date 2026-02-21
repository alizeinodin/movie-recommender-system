# Best Practices – ML, Backend, Frontend

## Why recommendations were changing on refresh (fixed)

1. **Backend fallback was random** – When the ML API was down, Laravel returned random movies per request.  
2. **No caching** – Each request recomputed or re-fetched recommendations.  
3. **User not persisted** – After refresh, the selected user could be lost.

**Fixes:** Backend caches recommendations per user (1 hour); deterministic fallback when ML is down; ML API in-memory cache; frontend persists user in `localStorage` and `useState`.

---

## Backend (Laravel) – Best practices

### API and validation
- **FormRequests**: Use `FormRequest` classes (e.g. `StoreRatingRequest`) for API payloads so validation and error shape live in one place.
- **Config for constants**: Use `config/recommender.php` (e.g. `user_id_min`, `user_id_max`) so controllers and validation share the same range.
- **Validate inputs**: Reject invalid `user_id` (e.g. 1–943 for MovieLens) and return `400` with a clear message. Validate `movie_id`, `rating` (1–5) in rating endpoints.
- **Consistent JSON**: Return stable shapes (e.g. `{ movies: [...] }`, paginated `{ data: [], last_page: N }`). Append computed fields (e.g. `poster_url`) via `$appends` or resources.
- **HTTP semantics**: Use `404` for missing resources, `400` for bad input, `503` when depending on an unavailable service (e.g. ML API).

### Configuration and environment
- **Config over env**: Read `ML_API_URL`, timeouts, etc. from `config/services.php` and `.env`. Never hardcode URLs or secrets.
- **Timeouts**: Use a reasonable timeout (e.g. 10s) when calling the ML API so the app doesn’t hang.

### Caching
- **Cache recommendations per user**: Use `Cache::remember` with a key like `recommendations:user:{id}` and a TTL (e.g. 1 hour) so the same user gets the same list across requests.
- **Deterministic fallback**: When the ML service is down, return a deterministic list (e.g. based on `user_id`) instead of random, so behaviour is reproducible.

### Logging and observability
- **Log ML failures**: When the ML API call fails, log a warning (e.g. `Log::warning`) with `user_id` and error message so you can debug without exposing internals to the client.
- **Structured logs**: Include context (user_id, endpoint) in log messages.

### Security and performance
- **CORS**: Restrict `allowed_origins` in production; allow only your frontend origin.
- **Rate limiting**: Consider throttling recommendation or rating endpoints if needed.
- **DB**: Use indexing on columns used in filters (e.g. `movie_id`, `user_id` for ratings).

---

## ML project – Best practices

### Reproducibility
- **Fixed seed**: Use a fixed random seed in training (e.g. `torch.manual_seed`, `np.random.seed`) and document it so runs are reproducible.
- **Requirements**: Pin or set minimum versions in `requirements.txt`; run training in a virtual environment and document the Python version.
- **Train/val/test split**: Use a fixed split (e.g. by random seed) and the same normalization (e.g. rating scale 1–5 → [0,1]) in training and inference.

### Inference
- **Deterministic inference**: Use `model.eval()` and `torch.no_grad()`; avoid dropout or stochastic layers at inference so the same input always gives the same output.
- **Single model load**: Load the model and mappings once at startup and reuse; avoid loading on every request.
- **Caching**: Cache recommendations per `(user_id, top_k)` in memory (or in Redis) so repeated requests return the same result and reduce load.

### API design
- **Health and readiness**: Expose `/health` (liveness) and `/ready` (model loaded, valid user range) so orchestrators and Laravel can check connectivity and correctness.
- **Validation**: Reject out-of-range `user_id` (e.g. 1–943) with `400` and a clear message. Return `503` when the model is not loaded.
- **Stable responses**: Return the same structure (e.g. `movie_ids`, `scores`) and document it.

### Operations
- **Request logging**: Use middleware to log request method, path, status, and duration for observability (e.g. `RequestLoggingMiddleware` in ml-api).
- **Check script**: Provide a script (e.g. `scripts/check_ml_api.py`) that calls `/health`, `/ready`, and `/recommend` for edge users so you can verify the API and that Laravel can connect for any user.
- **Errors**: Don’t expose stack traces to clients; log them server-side. Return short, safe error messages in API responses.

---

## Frontend (Nuxt)

- **Types**: Centralize API and domain types in `app/types.ts` (e.g. `Movie`, `MoviesResponse`, `ApiErrorBody`) and use them in composables and components.
- **Composables**: Use `useApi()` for all API calls and `useToast()` for success/error feedback (e.g. rating saved / failed).
- **User persistence**: Store selected user in `localStorage` and sync with URL query (`user_id`) so refresh keeps the same user and recommendations.
- **Shared state**: Use Nuxt `useState` for the current user so NavBar and pages share one source of truth.
- **Poster images**: Use `poster_url` from the API when present; fallback to a placeholder (gradient + initial) or placeholder image service on error.
- **Accessibility**: Semantic HTML, `aria-label` on controls, visible focus styles.
- **Loading and errors**: Show skeletons or loading state; handle API errors without breaking the UI.

---

## Movie posters and images

- **IMDB**: IMDB does **not** allow hotlinking to their images; avoid using IMDB image URLs directly.
- **FM-DB (seeder default)**: The seeder uses [FM-DB](https://imdb.iamidiotareyoutoo.com/docs/index.html) (`GET /search?q=<title>`) to fetch poster URLs; no API key. Config: `services.fmdb.base_url`.
- **TMDb / OMDb**: Prefer **TMDb** (themoviedb.org) or **OMDb** (omdbapi.com) for real posters: both offer APIs and allow linking to poster images. Store the poster URL (or path) in the backend (e.g. `poster_url` column or computed from an API call) and return it in the API; frontend keeps `@error` fallback to gradient/initial.
- **Placeholder**: Backend can return a placeholder URL (e.g. placehold.co with the movie title) so every movie has a visible image when you don’t have real assets yet. Frontend uses `<img>` with `@error` fallback to gradient + initial letter.
- **Backend**: `Movie::getPosterUrlAttribute()` can return a stored URL, a TMDb/OMDb URL, or a placeholder; keep the same JSON shape so the frontend always receives `poster_url`.

---

## UI and accessibility

- **User selector**: Use a custom dropdown (not a native `<select>`) if the list must be readable on both light and dark themes; native selects often render options with system styling (e.g. white text on light background). A custom list with dark background and white text ensures “User 196” and the User ID are always visible.
- **Contrast**: Keep sufficient contrast for body text (e.g. `text-gray-300` or `text-gray-400` on dark backgrounds). Use `focus-visible:ring` for keyboard focus.
- **Labels**: Show “User ID” or “User 196” explicitly where the current profile matters (e.g. navbar, rating section) so it’s clear whose recommendations and ratings are shown.
