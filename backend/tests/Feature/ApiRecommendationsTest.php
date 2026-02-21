<?php

namespace Tests\Feature;

use App\Models\Movie;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ApiRecommendationsTest extends TestCase
{
    use RefreshDatabase;

    private const API_V1 = '/api/v1';

    protected function setUp(): void
    {
        parent::setUp();
        Movie::create(['id' => 1, 'title' => 'Movie One']);
        Movie::create(['id' => 2, 'title' => 'Movie Two']);
    }

    public function test_recommendations_returns_json_with_movies(): void
    {
        $response = $this->getJson(self::API_V1 . '/recommendations/1');

        $response->assertStatus(200)->assertJsonStructure(['movies']);
        $this->assertIsArray($response->json('movies'));
    }

    public function test_recommendations_rejects_invalid_user_id(): void
    {
        $response = $this->getJson(self::API_V1 . '/recommendations/9999');

        $response->assertStatus(400)
            ->assertJson(['code' => 'INVALID_USER_ID']);
    }
}
