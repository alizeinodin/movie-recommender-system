<?php

use App\Http\Controllers\Api\MovieController;
use App\Http\Controllers\Api\RatingController;
use App\Http\Controllers\Api\RecommendationController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API v1 – Movie recommender (movies, ratings, recommendations)
|--------------------------------------------------------------------------
*/
Route::prefix('v1')->group(function (): void {
    Route::get('/movies', [MovieController::class, 'index']);
    Route::get('/movies/{id}', [MovieController::class, 'show'])->where('id', '[0-9]+');
    Route::get('/movies/{id}/rating', [RatingController::class, 'show'])->where('id', '[0-9]+');
    Route::get('/movies/{id}/similar', [MovieController::class, 'similar'])->where('id', '[0-9]+');
    Route::post('/ratings', [RatingController::class, 'store']);
    Route::get('/users/{userId}/ratings', [RatingController::class, 'userRatings'])->where('userId', '[0-9]+');
    Route::get('/recommendations/{userId}', [RecommendationController::class, 'index'])->where('userId', '[0-9]+');
});
