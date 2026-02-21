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

class RecommendationController extends Controller
{
    private const CACHE_TTL_SECONDS = 3600; // 1 hour – same user gets same list until expiry

    public function index(Request $request, int $userId): JsonResponse
    {
        $min = config('recommender.user_id_min', 1);
        $max = config('recommender.user_id_max', 943);
        if ($userId < $min || $userId > $max) {
            return response()->json([
                'message' => "Invalid user_id. Must be between {$min} and {$max}.",
                'code' => 'INVALID_USER_ID',
            ], 400);
        }

        $cacheKey = 'recommendations:user:' . $userId;
        // Use same top_k as demo (10) so frontend matches "python main.py demo"
        $topK = 10;
        $mlApiUrl = rtrim(config('services.ml_api.url', 'http://127.0.0.1:8000'), '/');
        $url = $mlApiUrl . '/recommend?user_id=' . $userId . '&top_k=' . $topK;

        try {
            $response = Http::timeout(10)->get($url);
            if ($response->successful()) {
                $data = $response->json();
                $movieIds = $data['movie_ids'] ?? [];
                if (!empty($movieIds)) {
                    $movies = Movie::whereIn('id', $movieIds)->get()->keyBy('id');
                    $ordered = collect($movieIds)->map(fn ($id) => $movies->get($id))->filter()->values();
                    $result = ['movies' => MovieResource::collection($ordered)->resolve()];
                    Cache::put($cacheKey, $result, self::CACHE_TTL_SECONDS);
                    return response()->json($result);
                }
            }
        } catch (\Throwable $e) {
            Log::warning('ML API recommendation failed, using fallback', [
                'user_id' => $userId,
                'error' => $e->getMessage(),
            ]);
        }

        $fallback = ['movies' => MovieResource::collection($this->fallbackRecommendationsList($userId))->resolve()];
        $cached = Cache::get($cacheKey);
        return response()->json($cached ?? $fallback);
    }

    /** Clear all recommendation caches (e.g. after ML API was down and served fallback). */
    public static function clearCache(): void
    {
        $min = config('recommender.user_id_min', 1);
        $max = config('recommender.user_id_max', 943);
        for ($userId = $min; $userId <= $max; $userId++) {
            Cache::forget('recommendations:user:' . $userId);
        }
    }

    /** Deterministic fallback so the same user always gets the same list (no random). */
    private function fallbackRecommendationsList(int $userId): array
    {
        $total = Movie::count();
        if ($total === 0) {
            return [];
        }
        $limit = min(10, $total);
        $maxOffset = max(0, $total - $limit);
        $offset = $maxOffset > 0 ? abs(crc32((string) $userId)) % ($maxOffset + 1) : 0;
        return Movie::query()->orderBy('id')->offset($offset)->limit($limit)->get()->all();
    }
}
