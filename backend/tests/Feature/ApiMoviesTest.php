<?php

namespace Tests\Feature;

use App\Models\Movie;
use App\Models\Rating;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ApiMoviesTest extends TestCase
{
    use RefreshDatabase;

    private const API_V1 = '/api/v1';

    protected function setUp(): void
    {
        parent::setUp();
        Movie::create(['id' => 1, 'title' => 'Test Movie']);
    }

    public function test_movies_index_returns_paginated_json(): void
    {
        $response = $this->getJson(self::API_V1 . '/movies?per_page=5');

        $response->assertStatus(200)
            ->assertJsonStructure([
                'data' => [
                    '*' => ['id', 'title', 'release_date', 'genres', 'poster_url', 'overview', 'runtime', 'imdb_id', 'backdrop_url'],
                ],
                'meta' => ['current_page', 'last_page', 'per_page', 'total'],
            ]);
    }

    public function test_movies_show_returns_movie(): void
    {
        $response = $this->getJson(self::API_V1 . '/movies/1');

        $response->assertStatus(200)
            ->assertJsonFragment(['id' => 1, 'title' => 'Test Movie']);
    }

    public function test_movies_show_returns_404_for_missing(): void
    {
        $response = $this->getJson(self::API_V1 . '/movies/99999');

        $response->assertStatus(404)
            ->assertJson(['message' => 'Movie not found', 'code' => 'MOVIE_NOT_FOUND']);
    }

    public function test_movies_similar_returns_json_with_movies(): void
    {
        $response = $this->getJson(self::API_V1 . '/movies/1/similar');

        $response->assertStatus(200)->assertJsonStructure(['movies']);
        $this->assertIsArray($response->json('movies'));
    }

    public function test_movies_similar_returns_404_for_missing_movie(): void
    {
        $response = $this->getJson(self::API_V1 . '/movies/99999/similar');

        $response->assertStatus(404)
            ->assertJson(['message' => 'Movie not found', 'code' => 'MOVIE_NOT_FOUND']);
    }
}
