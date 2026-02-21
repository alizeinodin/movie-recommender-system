<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Rating extends Model
{
    protected $fillable = ['user_id', 'movie_id', 'rating'];

    public function movie()
    {
        return $this->belongsTo(Movie::class);
    }
}
