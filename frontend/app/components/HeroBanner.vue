<template>
  <section class="relative w-full h-[45vw] min-h-[320px] max-h-[560px] -mx-4 sm:-mx-6 md:-mx-8 mb-10 overflow-hidden rounded-b-2xl md:rounded-b-3xl">
    <!-- Backdrop image or gradient -->
    <div v-if="backdropUrl" class="absolute inset-0">
      <img
        :src="backdropUrl"
        :alt="title"
        class="w-full h-full object-cover scale-105"
      >
    </div>
    <div v-else class="absolute inset-0 bg-gray-900" :style="gradientStyle" />
    <!-- Overlays -->
    <div class="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent z-10" />
    <div class="absolute inset-0 bg-gradient-to-r from-black/90 via-black/40 to-transparent z-10" />
    <!-- Content -->
    <div class="absolute inset-0 flex items-end md:items-center px-6 sm:px-8 md:px-12 lg:px-16 z-20 pb-12 md:pb-16">
      <div class="max-w-2xl">
        <p v-if="year" class="text-primary font-semibold text-sm uppercase tracking-widest mb-2">
          {{ year }}
        </p>
        <h1 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-white drop-shadow-2xl mb-4 font-serif leading-tight">
          {{ title }}
        </h1>
        <p v-if="subtitle" class="text-gray-300 text-base sm:text-lg mb-6 max-w-lg">
          {{ subtitle }}
        </p>
        <p v-if="genres" class="text-gray-400 text-sm mb-6">
          {{ genres }}
        </p>
        <div class="flex flex-wrap gap-3">
          <NuxtLink
            v-if="movieId && userId"
            :to="`/movies/${movieId}?user_id=${userId}`"
            class="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-primary text-white font-semibold hover:bg-red-600 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-black/50 shadow-lg shadow-primary/20"
          >
            View details
          </NuxtLink>
          <NuxtLink
            v-if="movieId && userId"
            :to="`/movies/${movieId}?user_id=${userId}`"
            class="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-white/15 text-white font-medium border border-white/30 hover:bg-white/25 transition-colors backdrop-blur"
          >
            Rate & recommend
          </NuxtLink>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    title: string
    subtitle?: string
    movieId?: number
    userId?: number
    backdropUrl?: string | null
    year?: string | number | null
    genres?: string | null
    /** Used for gradient fallback when no image */
    movieIdForGradient?: number
  }>(),
  { subtitle: '', movieId: undefined, userId: undefined, backdropUrl: null, year: null, genres: '', movieIdForGradient: 0 }
)

const hue = computed(() => (props.movieIdForGradient * 137.508) % 360)
const gradientStyle = computed(() => ({
  background: `linear-gradient(135deg, hsl(${hue.value}, 40%, 18%) 0%, #0d0d0d 100%)`,
}))
</script>
