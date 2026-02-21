<?php

return [

    /*
    |--------------------------------------------------------------------------
    | Third Party Services
    |--------------------------------------------------------------------------
    |
    | This file is for storing the credentials for third party services such
    | as Mailgun, Postmark, AWS and more. This file provides the de facto
    | location for this type of information, allowing packages to have
    | a conventional file to locate the various service credentials.
    |
    */

    'postmark' => [
        'key' => env('POSTMARK_API_KEY'),
    ],

    'resend' => [
        'key' => env('RESEND_API_KEY'),
    ],

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    ],

    'slack' => [
        'notifications' => [
            'bot_user_oauth_token' => env('SLACK_BOT_USER_OAUTH_TOKEN'),
            'channel' => env('SLACK_BOT_USER_DEFAULT_CHANNEL'),
        ],
    ],

    'ml_api' => [
        'url' => env('ML_API_URL', 'http://127.0.0.1:8000'),
    ],

    'tmdb' => [
        'api_key' => env('TMDB_API_KEY'),
        'base_url' => 'https://api.themoviedb.org/3',
        'image_base' => 'https://image.tmdb.org/t/p/w500',
    ],

    /*
    | FM-DB (Free Movie DB) – no API key. Used by MovieLensSeeder for poster URLs.
    | Docs: https://imdb.iamidiotareyoutoo.com/docs/index.html
    */
    'fmdb' => [
        'base_url' => env('FMDB_API_URL', 'https://imdb.iamidiotareyoutoo.com'),
    ],

];
