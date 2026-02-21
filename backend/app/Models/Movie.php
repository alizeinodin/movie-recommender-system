<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Str;

class Movie extends Model
{
    public $incrementing = false;

    protected $keyType = 'integer';

    protected $fillable = ['id', 'title', 'release_date', 'genres', 'poster_url', 'overview', 'runtime', 'imdb_id', 'backdrop_url'];

    protected $casts = [
        'release_date' => 'date',
    ];

    /** @var list<string> */
    protected $appends = ['poster_url'];

    public function ratings()
    {
        return $this->hasMany(Rating::class);
    }

    /**
     * Poster URL for the UI. Uses stored poster_url from DB (e.g. from TMDb) when set;
     * otherwise returns a placeholder image so every movie has a visible image.
     */
    public function getPosterUrlAttribute(): ?string
    {
        $stored = $this->attributes['poster_url'] ?? null;
        if ($stored !== null && $stored !== '') {
            return $stored;
        }
        $title = Str::limit($this->title ?? 'Movie', 28);
        $encoded = str_replace(' ', '+', rawurlencode($title));

        return 'https://placehold.co/300x450/1a1a2e/94a3b8?text=' . $encoded;
    }
}
