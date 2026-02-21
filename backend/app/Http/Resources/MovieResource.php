<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class MovieResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'release_date' => $this->release_date?->format('Y-m-d'),
            'genres' => $this->genres,
            'poster_url' => $this->poster_url,
            'overview' => $this->overview,
            'runtime' => $this->runtime,
            'imdb_id' => $this->imdb_id,
            'backdrop_url' => $this->backdrop_url,
        ];
    }
}
