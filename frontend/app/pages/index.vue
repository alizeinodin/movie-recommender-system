<template>
  <div class="min-h-screen bg-[#141414]">
    <AppNavBar />
    <main class="pt-20 pb-16">
      <!-- Hero: first recommended or first movie with backdrop image -->
      <div class="px-4 sm:px-6 md:px-8">
        <HeroBanner
          :title="heroTitle"
          :subtitle="heroSubtitle"
          :movie-id="heroMovieId"
          :user-id="userId"
          :backdrop-url="heroPosterUrl"
          :year="heroYear"
          :genres="heroGenres"
          :movie-id-for-gradient="heroMovieId || 0"
        />
      </div>

      <!-- Recommended for you -->
      <section class="px-4 sm:px-6 md:px-8 mb-14">
        <CarouselSection title="Recommended for you" :subtitle="`Personalized for User ${userId}`">
          <template v-if="recommendationsLoading">
            <div v-for="i in 8" :key="i" class="w-32 sm:w-36 md:w-40 shrink-0 aspect-[2/3] rounded-lg bg-gray-800/80 animate-pulse" />
          </template>
          <template v-else>
            <div v-for="m in recommendations" :key="m.id" class="w-32 sm:w-36 md:w-40 shrink-0">
              <MovieCard :movie="m" :user-id="userId" />
            </div>
          </template>
        </CarouselSection>
      </section>

      <!-- All movies -->
      <section class="px-4 sm:px-6 md:px-8 mb-14">
        <div class="mb-6">
          <h2 class="text-2xl font-bold text-white tracking-tight">
            All movies
          </h2>
          <p class="text-gray-400 text-sm mt-1">Browse and rate the catalog</p>
        </div>
        <div v-if="moviesLoading" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4 md:gap-5">
          <div v-for="i in 12" :key="i" class="aspect-[2/3] rounded-xl bg-gray-800/80 animate-pulse" />
        </div>
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4 md:gap-5">
          <MovieCard v-for="m in movies" :key="m.id" :movie="m" :user-id="userId" />
        </div>
        <div v-if="hasMore" class="mt-10 text-center">
          <button
            class="px-10 py-3.5 rounded-xl bg-primary hover:bg-red-600 text-white font-semibold text-sm transition-colors disabled:opacity-50 shadow-lg shadow-primary/20"
            :disabled="loadingMore"
            @click="loadMore"
          >
            {{ loadingMore ? 'Loading…' : 'Load more' }}
          </button>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import type { Movie } from '~/types'

useSeoMeta({
  title: 'MovieBox – Movie recommender',
  description: 'Personalized movie recommendations powered by deep learning (NCF). Browse and rate movies.',
})

const { getMovies, getRecommendations } = useApi()
const { userId } = usePersistedUser()

const recommendations = ref<Movie[]>([])
const recommendationsLoading = ref(true)
const movies = ref<Movie[]>([])
const moviesLoading = ref(true)
const loadingMore = ref(false)
const currentPage = ref(1)
const lastPage = ref(1)
const hasMore = computed(() => currentPage.value < lastPage.value)

const heroMovie = computed(() => recommendations.value[0] ?? movies.value[0] ?? null)
const heroMovieId = computed(() => heroMovie.value?.id ?? 0)
const heroTitle = computed(() => heroMovie.value?.title ?? 'MovieBox')
const heroSubtitle = computed(() => (recommendations.value.length ? 'Top pick for you' : 'Browse and rate movies'))
const heroPosterUrl = computed(() => heroMovie.value?.poster_url ?? null)
const heroYear = computed(() => {
  const d = heroMovie.value?.release_date
  return d ? new Date(d).getFullYear() : null
})
const heroGenres = computed(() => heroMovie.value?.genres ?? '')

async function fetchRecommendations() {
  recommendationsLoading.value = true
  try {
    const r = await getRecommendations(userId.value)
    recommendations.value = r.movies ?? []
  } catch {
    recommendations.value = []
  }
  recommendationsLoading.value = false
}

async function fetchMovies(page = 1) {
  if (page === 1) moviesLoading.value = true
  else loadingMore.value = true
  try {
    const r = await getMovies(page, 24)
    const list = r.data ?? []
    if (page === 1) movies.value = list
    else movies.value.push(...list)
    lastPage.value = r.last_page ?? r.meta?.last_page ?? 1
    currentPage.value = page
  } catch {
    if (page === 1) movies.value = []
  }
  moviesLoading.value = false
  loadingMore.value = false
}

function loadMore() {
  fetchMovies(currentPage.value + 1)
}

watch(userId, () => fetchRecommendations())

onMounted(() => {
  fetchRecommendations()
  fetchMovies(1)
})
</script>
