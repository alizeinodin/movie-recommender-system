<?php

use Illuminate\Foundation\Inspiring;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Cache;

Artisan::command('inspire', function () {
    $this->comment(Inspiring::quote());
})->purpose('Display an inspiring quote');

Artisan::command('recommendations:clear-cache', function () {
    for ($userId = 1; $userId <= 943; $userId++) {
        Cache::forget('recommendations:user:' . $userId);
    }
    $this->info('Recommendation cache cleared. Frontend will now get fresh results from the ML API.');
})->purpose('Clear recommendation cache so frontend matches "python main.py demo" (run when ML API is up)');
