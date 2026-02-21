/**
 * Shared API and domain types for the frontend.
 */

export interface Movie {
  id: number
  title: string
  release_date?: string
  genres?: string
  poster_url?: string | null
  overview?: string | null
  runtime?: number | null
  imdb_id?: string | null
  backdrop_url?: string | null
}

export interface ApiPaginated<T> {
  data: T[]
  meta: {
    current_page: number
    last_page: number
    per_page: number
    total: number
  }
  links?: unknown
}

export interface MoviesResponse {
  data: Movie[]
  meta: { current_page: number; last_page: number; per_page: number; total: number }
  links?: unknown
  last_page: number
}

export interface RecommendationsResponse {
  movies: Movie[]
}

export interface RatingResponse {
  rating: number | null
}

export interface ApiErrorBody {
  message: string
  code?: string
  errors?: Record<string, string[]>
}
