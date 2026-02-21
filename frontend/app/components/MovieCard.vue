<template>
  <NuxtLink
    :to="`/movies/${movie.id}?user_id=${userId}`"
    class="group block focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-[#111] rounded-xl"
  >
    <div
      class="relative aspect-[2/3] w-full rounded-xl overflow-hidden bg-gray-900 border border-gray-800/60 shadow-lg transition-all duration-300 group-hover:scale-[1.03] group-hover:border-gray-700 group-hover:shadow-xl group-hover:shadow-black/50 group-hover:z-10"
    >
      <MoviePoster :movie-id="movie.id" :title="movie.title" :poster-url="movie.poster_url" />
      <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
      <div class="absolute bottom-0 left-0 right-0 p-3 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
        <p class="text-white text-sm font-medium line-clamp-2 drop-shadow-lg">
          {{ movie.title }}
        </p>
      </div>
    </div>
    <p class="mt-2 text-sm font-medium truncate text-gray-300 group-hover:text-white transition-colors px-0.5">
      {{ movie.title }}
    </p>
  </NuxtLink>
</template>

<script setup lang="ts">
import type { Movie } from '~/types'

defineProps<{
  movie: Movie
  userId: number
}>()
</script>
