<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('movies', function (Blueprint $table) {
            $table->unsignedInteger('id')->primary(); // MovieLens movie_id
            $table->string('title');
            $table->date('release_date')->nullable();
            $table->string('genres')->nullable(); // comma-separated for simplicity
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('movies');
    }
};
