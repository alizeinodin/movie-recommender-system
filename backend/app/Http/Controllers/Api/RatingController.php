<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\Api\StoreRatingRequest;
use App\Http\Resources\RatingResource;
use App\Models\Rating;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;

class RatingController extends Controller
{
    public function show(int $id, Request $request): JsonResponse
    {
        $userId = (int) $request->get('user_id');
        if (!$userId) {
            return response()->json(['rating' => null]);
        }
        $rating = Rating::where('movie_id', $id)->where('user_id', $userId)->first();
        return response()->json(['rating' => $rating?->rating ?? null]);
    }

    public function store(StoreRatingRequest $request): JsonResponse
    {
        $validated = $request->validated();

        $rating = Rating::updateOrCreate(
            [
                'user_id' => $validated['user_id'],
                'movie_id' => $validated['movie_id'],
            ],
            ['rating' => $validated['rating']]
        );

        Cache::forget('recommendations:user:' . $validated['user_id']);

        return (new RatingResource($rating))->response()->setStatusCode(201);
    }

    public function userRatings(int $userId): JsonResponse
    {
        $ratings = Rating::where('user_id', $userId)
            ->with('movie:id,title')
            ->get()
            ->map(fn ($r) => [
                'movie_id' => $r->movie_id,
                'rating' => $r->rating,
                'title' => $r->movie?->title,
            ]);

        return response()->json(['ratings' => $ratings]);
    }
}
