<template>
  <div class="min-h-screen bg-[#0f0f0f]">
    <AppNavBar />

    <!-- Movie detail: backdrop + content -->
    <main v-if="movie" class="pt-20">
      <!-- Backdrop hero (prefer backdrop_url, else poster_url) -->
      <section class="relative w-full h-[50vw] min-h-[280px] max-h-[480px] overflow-hidden">
        <div v-if="heroImageUrl" class="absolute inset-0">
          <img
            :src="heroImageUrl"
            :alt="movie.title"
            class="w-full h-full object-cover scale-105"
          >
        </div>
        <div v-else class="absolute inset-0 bg-gray-900" :style="backdropGradient" />
        <div class="absolute inset-0 bg-gradient-to-t from-[#0f0f0f] via-[#0f0f0f]/80 to-transparent z-10" />
        <div class="absolute inset-0 bg-gradient-to-r from-[#0f0f0f]/90 via-[#0f0f0f]/50 to-transparent z-10" />
        <div class="absolute bottom-0 left-0 right-0 p-6 sm:p-8 md:p-10 z-20">
          <div class="max-w-4xl">
            <p v-if="movie.release_date" class="text-primary font-semibold text-sm uppercase tracking-widest mb-2">
              {{ movieYear }}
            </p>
            <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold text-white font-serif drop-shadow-2xl mb-3">
              {{ movie.title }}
            </h1>
            <div v-if="movie.genres" class="flex flex-wrap gap-2 mb-4">
              <span
                v-for="g in genreList"
                :key="g"
                class="px-3 py-1 rounded-full bg-white/15 text-gray-300 text-xs font-medium"
              >
                {{ g }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Content card -->
      <section class="relative -mt-24 z-30 px-4 sm:px-6 md:px-8 pb-16">
        <div class="max-w-5xl mx-auto">
          <div class="flex flex-col md:flex-row gap-8 md:gap-10 p-6 sm:p-8 rounded-2xl bg-gray-900/80 border border-gray-800/80 shadow-2xl backdrop-blur">
            <!-- Poster (smaller on detail) -->
            <div class="md:w-52 shrink-0 aspect-[2/3] rounded-xl overflow-hidden bg-gray-800 shadow-xl ring-2 ring-white/10">
              <MoviePoster :movie-id="movie.id" :title="movie.title" :poster-url="movie.poster_url" />
            </div>

            <div class="flex-1 min-w-0">
              <div class="mb-8">
                <h2 class="text-sm font-medium text-gray-400 uppercase tracking-wider mb-2">Your rating</h2>
                <StarsRate :model-value="userRating" @update:model-value="onRate" />
                <p v-if="toast.message && !toast.isError" class="mt-2 text-sm text-green-400">{{ toast.message }}</p>
                <p v-else-if="toast.message && toast.isError" class="mt-2 text-sm text-red-400">{{ toast.message }}</p>
              </div>

              <div class="mb-8">
                <h2 class="text-sm font-medium text-gray-400 uppercase tracking-wider mb-2">Overview</h2>
                <p v-if="movie.overview" class="text-gray-300 text-sm leading-relaxed">{{ movie.overview }}</p>
                <p v-else class="text-gray-500 text-sm italic">No overview available for this movie.</p>
              </div>

              <div class="mb-8">
                <h2 class="text-sm font-medium text-gray-400 uppercase tracking-wider mb-2">Details</h2>
                <dl class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
                  <div v-if="movie.release_date">
                    <dt class="text-gray-500">Release date</dt>
                    <dd class="text-white font-medium">{{ movieYear }} ({{ movie.release_date }})</dd>
                  </div>
                  <div v-if="movie.runtime">
                    <dt class="text-gray-500">Runtime</dt>
                    <dd class="text-white font-medium">{{ movie.runtime }} min</dd>
                  </div>
                  <div v-if="movie.genres">
                    <dt class="text-gray-500">Genres</dt>
                    <dd class="text-white font-medium">{{ movie.genres }}</dd>
                  </div>
                  <div v-if="movie.imdb_id">
                    <dt class="text-gray-500">IMDb</dt>
                    <dd class="text-white font-medium">
                      <a
                        :href="`https://www.imdb.com/title/${movie.imdb_id}/`"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="text-primary hover:underline"
                      >
                        {{ movie.imdb_id }} ↗
                      </a>
                    </dd>
                  </div>
                  <div>
                    <dt class="text-gray-500">Movie ID</dt>
                    <dd class="text-white font-medium">{{ movie.id }}</dd>
                  </div>
                  <div>
                    <dt class="text-gray-500">Your profile</dt>
                    <dd class="text-white font-medium">User {{ userId }}</dd>
                  </div>
                </dl>
              </div>

              <NuxtLink
                :to="{ path: '/', query: { user_id: String(userId) } }"
                class="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-primary hover:bg-red-600 text-white font-semibold text-sm transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-gray-900"
              >
                ← Back to home
              </NuxtLink>
            </div>
          </div>

          <!-- More like this -->
          <div v-if="moreLikeThis.length > 0" class="mt-14">
            <h2 class="text-2xl font-bold text-white tracking-tight mb-2">More like this</h2>
            <p class="text-gray-400 text-sm mb-6">Movies similar to this one</p>
            <CarouselSection title="More like this" :hide-nav="false" :hide-header="true">
              <div v-for="m in moreLikeThis" :key="m.id" class="w-36 sm:w-40 shrink-0">
                <MovieCard :movie="m" :user-id="userId" />
              </div>
            </CarouselSection>
          </div>
        </div>
      </section>
    </main>

    <main v-else-if="loading" class="pt-24 px-8">
      <div class="max-w-3xl mx-auto h-80 rounded-2xl bg-gray-800/80 animate-pulse" />
    </main>

    <main v-else class="pt-24 px-8 pb-16">
      <div class="max-w-3xl mx-auto text-center py-16">
        <h1 class="text-2xl font-bold text-white mb-4">Movie not found</h1>
        <p class="text-gray-400 mb-8">The movie you're looking for doesn't exist or was removed.</p>
        <NuxtLink
          :to="{ path: '/', query: userId ? { user_id: String(userId) } : {} }"
          class="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-primary hover:bg-red-600 text-white font-semibold transition-colors"
        >
          Back to home
        </NuxtLink>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import type { Movie } from '~/types'

const route = useRoute()
const { getMovie, getMovieRating, getSimilarMovies, submitRating } = useApi()
const toast = useToast()

const id = computed(() => Number(route.params.id))
const movie = ref<Movie | null>(null)
const loading = ref(true)
const userRating = ref<number | null>(null)
const { userId } = usePersistedUser()
const moreLikeThis = ref<Movie[]>([])

const movieYear = computed(() =>
  movie.value?.release_date ? new Date(movie.value.release_date).getFullYear() : null
)
const genreList = computed(() => {
  const g = movie.value?.genres
  if (!g) return []
  return g.split(',').map((s) => s.trim()).filter(Boolean)
})
const heroImageUrl = computed(() =>
  movie.value?.backdrop_url || movie.value?.poster_url || null
)
const backdropGradient = computed(() => {
  const hue = ((movie.value?.id ?? 0) * 137.508) % 360
  return {
    background: `linear-gradient(135deg, hsl(${hue}, 40%, 18%) 0%, #0d0d0d 100%)`,
  }
})

async function fetchMovie() {
  loading.value = true
  try {
    movie.value = await getMovie(id.value)
  } catch {
    movie.value = null
  }
  loading.value = false
}

async function fetchUserRating() {
  try {
    const r = await getMovieRating(id.value, userId.value)
    userRating.value = r.rating
  } catch {
    userRating.value = null
  }
}

async function fetchMoreLikeThis() {
  try {
    const r = await getSimilarMovies(id.value)
    moreLikeThis.value = r.movies ?? []
  } catch {
    moreLikeThis.value = []
  }
}

async function onRate(rating: number) {
  userRating.value = rating
  toast.clear()
  try {
    await submitRating(userId.value, id.value, rating)
    toast.success('Rating saved.')
  } catch (e: unknown) {
    const body = (e as { data?: unknown })?.data
    const msg =
      typeof body === 'object' && body !== null && 'message' in body
        ? String((body as { message: string }).message)
        : 'Failed to save rating.'
    toast.error(msg)
  }
}

async function loadPage() {
  await fetchMovie()
  if (movie.value) {
    fetchUserRating()
    fetchMoreLikeThis()
  }
}

onMounted(() => loadPage())

watch(id, () => loadPage())
watch(userId, () => { if (movie.value) fetchUserRating() })

useSeoMeta({
  title: computed(() =>
    movie.value?.title ? `${movie.value.title} · MovieBox` : 'Movie · MovieBox'
  ),
  description: computed(() =>
    movie.value?.overview?.trim()
      ? String(movie.value.overview).slice(0, 160)
      : movie.value?.title
        ? `Rate and get recommendations for ${movie.value.title}.`
        : 'Movie details on MovieBox.'
  ),
})
</script>
