import type {
  Movie,
  MoviesResponse,
  RecommendationsResponse,
  RatingResponse,
  ApiErrorBody,
} from '~/types'

export function useApi() {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase as string

  async function getMovies(page = 1, perPage = 24): Promise<MoviesResponse> {
    const res = await $fetch<MoviesResponse & { meta: { last_page: number } }>(
      `${apiBase}/movies?per_page=${perPage}&page=${page}`
    )
    return { ...res, last_page: res.meta?.last_page ?? 1 }
  }

  async function getMovie(id: number): Promise<Movie> {
    const res = await $fetch<{ data?: Movie } | Movie>(`${apiBase}/movies/${id}`)
    return ('data' in res && res.data) ? res.data : (res as Movie)
  }

  async function getRecommendations(userId: number): Promise<RecommendationsResponse> {
    return $fetch<RecommendationsResponse>(`${apiBase}/recommendations/${userId}`)
  }

  async function getSimilarMovies(movieId: number): Promise<RecommendationsResponse> {
    return $fetch<RecommendationsResponse>(`${apiBase}/movies/${movieId}/similar`)
  }

  async function getMovieRating(movieId: number, userId: number): Promise<RatingResponse> {
    return $fetch<RatingResponse>(`${apiBase}/movies/${movieId}/rating?user_id=${userId}`)
  }

  async function submitRating(userId: number, movieId: number, rating: number): Promise<void> {
    await $fetch(`${apiBase}/ratings`, {
      method: 'POST',
      body: { user_id: userId, movie_id: movieId, rating },
    })
  }

  return {
    apiBase,
    getMovies,
    getMovie,
    getRecommendations,
    getSimilarMovies,
    getMovieRating,
    submitRating,
  }
}

/** Type guard for API error response body. */
export function isApiErrorBody(body: unknown): body is ApiErrorBody {
  return (
    typeof body === 'object' &&
    body !== null &&
    'message' in body &&
    typeof (body as ApiErrorBody).message === 'string'
  )
}
