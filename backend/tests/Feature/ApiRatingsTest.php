<?php

namespace Tests\Feature;

use App\Models\Movie;
use App\Models\Rating;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ApiRatingsTest extends TestCase
{
    use RefreshDatabase;

    private const API_V1 = '/api/v1';

    protected function setUp(): void
    {
        parent::setUp();
        Movie::create(['id' => 1, 'title' => 'Test Movie']);
    }

    public function test_rating_show_returns_null_when_no_user_id(): void
    {
        $response = $this->getJson(self::API_V1 . '/movies/1/rating');

        $response->assertStatus(200)
            ->assertJson(['rating' => null]);
    }

    public function test_rating_store_creates_rating(): void
    {
        $response = $this->postJson(self::API_V1 . '/ratings', [
            'user_id' => 1,
            'movie_id' => 1,
            'rating' => 4,
        ]);

        $response->assertStatus(201)
            ->assertJsonFragment(['user_id' => 1, 'movie_id' => 1, 'rating' => 4]);

        $this->assertDatabaseHas('ratings', [
            'user_id' => 1,
            'movie_id' => 1,
            'rating' => 4,
        ]);
    }

    public function test_rating_store_validation_error(): void
    {
        $response = $this->postJson(self::API_V1 . '/ratings', [
            'user_id' => 1,
            'movie_id' => 1,
            'rating' => 10, // invalid: max 5
        ]);

        $response->assertStatus(422)
            ->assertJson(['code' => 'VALIDATION_ERROR'])
            ->assertJsonStructure(['errors']);
    }
}
