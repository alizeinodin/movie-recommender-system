<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('movies', function (Blueprint $table) {
            $table->text('overview')->nullable()->after('poster_url');
            $table->unsignedSmallInteger('runtime')->nullable()->after('overview');
            $table->string('imdb_id', 20)->nullable()->after('runtime');
            $table->string('backdrop_url', 500)->nullable()->after('imdb_id');
        });
    }

    public function down(): void
    {
        Schema::table('movies', function (Blueprint $table) {
            $table->dropColumn(['overview', 'runtime', 'imdb_id', 'backdrop_url']);
        });
    }
};
