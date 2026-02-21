<?php

namespace Database\Seeders;

use App\Models\Movie;
use App\Models\Rating;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Http;

class MovieLensSeeder extends Seeder
{
    public function run(): void
    {
        // MovieLens data lives in ml-api/data/ml-100k (moved from project root)
        $dataDir = base_path('../ml-api/data/ml-100k');
        $itemPath = $dataDir . '/u.item';
        $dataPath = $dataDir . '/u.data';

        if (!is_file($itemPath) || !is_file($dataPath)) {
            $this->command->warn("MovieLens data not found at {$dataDir}. Skipping seed.");
            return;
        }

        // Parse u.item: movie_id|title|release_date|...
        $genres = ['Unknown', 'Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime',
            'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
            'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'];

        $lines = file($itemPath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        foreach ($lines as $line) {
            $parts = explode('|', $line);
            if (count($parts) < 2) continue;
            $movieId = (int) $parts[0];
            $title = $parts[1];
            $releaseDate = null;
            if (!empty($parts[2]) && $parts[2] !== '') {
                $d = \DateTime::createFromFormat('d-M-Y', trim($parts[2]));
                $releaseDate = $d ? $d->format('Y-m-d') : null;
            }
            $genreBits = array_slice($parts, 5, 19);
            $movieGenres = [];
            foreach ($genreBits as $i => $bit) {
                if (isset($genres[$i]) && (int)$bit === 1) {
                    $movieGenres[] = $genres[$i];
                }
            }
            Movie::updateOrCreate(
                ['id' => $movieId],
                [
                    'title' => $title,
                    'release_date' => $releaseDate,
                    'genres' => implode(', ', $movieGenres),
                ]
            );
        }

        $this->command->info('Movies seeded: ' . Movie::count());

        // Parse u.data: user_id \t item_id \t rating \t timestamp
        Rating::query()->delete();
        $fh = fopen($dataPath, 'r');
        $chunk = [];
        while (($line = fgets($fh)) !== false) {
            $cols = preg_split('/\s+/', trim($line), 4);
            if (count($cols) >= 3) {
                $chunk[] = [
                    'user_id' => (int) $cols[0],
                    'movie_id' => (int) $cols[1],
                    'rating' => (int) $cols[2],
                ];
            }
            if (count($chunk) >= 2000) {
                $now = now();
                foreach ($chunk as &$r) {
                    $r['created_at'] = $r['updated_at'] = $now;
                }
                Rating::insert($chunk);
                $chunk = [];
            }
        }
        fclose($fh);
        if (!empty($chunk)) {
            $now = now();
            foreach ($chunk as &$r) {
                $r['created_at'] = $r['updated_at'] = $now;
            }
            Rating::insert($chunk);
        }

        $this->command->info('Ratings seeded: ' . Rating::count());

        // Fetch poster URLs from FM-DB (Free Movie DB) – no API key required
        $this->fetchPostersFromFmDb();
    }

    /**
     * Fetch poster URLs from FM-DB API (https://imdb.iamidiotareyoutoo.com).
     * Uses GET /search?q=<title>. Response: { "ok": true, "description": [ { "#IMG_POSTER": "url", ... } ] }.
     */
    private function fetchPostersFromFmDb(): void
    {
        $baseUrl = rtrim(config('services.fmdb.base_url', 'https://imdb.iamidiotareyoutoo.com'), '/');
        $movies = Movie::all();
        $updated = 0;

        foreach ($movies as $movie) {
            // Strip year from title for better match, e.g. "Toy Story (1995)" -> "Toy Story"
            $query = preg_replace('/\s*\(\d{4}\)\s*$/', '', $movie->title);
            $query = trim($query);
            if ($query === '') {
                continue;
            }

            $response = Http::timeout(15)->get($baseUrl . '/search', [
                'q' => $query,
            ]);

            if (!$response->successful()) {
                continue;
            }

            $data = $response->json();
            if (!($data['ok'] ?? false) || empty($data['description']) || !is_array($data['description'])) {
                continue;
            }

            $posterUrl = null;
            foreach ($data['description'] as $item) {
                $url = $item['#IMG_POSTER'] ?? $item['#img_poster'] ?? null;
                if (!empty($url) && is_string($url)) {
                    $posterUrl = $url;
                    break;
                }
            }

            if ($posterUrl !== null) {
                $movie->poster_url = $posterUrl;
                $movie->save();
                $updated++;
            }

            // Throttle to avoid hammering the API
            usleep(250000); // 0.25 sec
        }

        $this->command->info("Poster URLs updated from FM-DB: {$updated} / " . $movies->count());
    }
}
