<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\MovieResource;
use App\Models\Movie;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class MovieController extends Controller
{
    private const SIMILAR_CACHE_TTL_SECONDS = 3600;

    public function index(Request $request): JsonResponse
    {
        $perPage = min((int) $request->get('per_page', 24), 100);
        $perPage = max(1, $perPage);
        $movies = Movie::query()
            ->orderBy('id')
            ->paginate($perPage);

        return MovieResource::collection($movies)->response();
    }

    public function show(int $id): JsonResponse
    {
        $movie = Movie::find($id);
        if (! $movie) {
            return response()->json([
                'message' => 'Movie not found',
                'code' => 'MOVIE_NOT_FOUND',
            ], 404);
        }

        return (new MovieResource($movie))->response();
    }

    /** Movies similar to the given movie (from ML API item-based similarity). */
    public function similar(int $id): JsonResponse
    {
        $movie = Movie::find($id);
        if (! $movie) {
            return response()->json([
                'message' => 'Movie not found',
                'code' => 'MOVIE_NOT_FOUND',
            ], 404);
        }

        $cacheKey = 'similar:movie:' . $id;
        $cached = Cache::get($cacheKey);
        if ($cached !== null) {
            return response()->json($cached);
        }

        $mlApiUrl = rtrim(config('services.ml_api.url', 'http://127.0.0.1:8000'), '/');
        $topK = 12;
        $url = $mlApiUrl . '/similar?movie_id=' . $id . '&top_k=' . $topK;

        try {
            $response = Http::timeout(10)->get($url);
            if ($response->successful()) {
                $data = $response->json();
                $movieIds = $data['movie_ids'] ?? [];
                if (! empty($movieIds)) {
                    $movies = Movie::whereIn('id', $movieIds)->get()->keyBy('id');
                    $ordered = collect($movieIds)->map(fn ($mid) => $movies->get($mid))->filter()->values();
                    $result = ['movies' => MovieResource::collection($ordered)->resolve()];
                    Cache::put($cacheKey, $result, self::SIMILAR_CACHE_TTL_SECONDS);

                    return response()->json($result);
                }
            }
        } catch (\Throwable $e) {
            Log::warning('ML API similar movies failed', ['movie_id' => $id, 'error' => $e->getMessage()]);
        }

        $fallback = Movie::query()
            ->where('id', '!=', $id)
            ->orderBy('id')
            ->limit($topK)
            ->get();
        $result = ['movies' => MovieResource::collection($fallback)->resolve()];

        return response()->json($result);
    }
}
