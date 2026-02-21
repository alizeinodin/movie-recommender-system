// https://nuxt.com/docs/api/configuration/nuxt-config
// Inspired by https://github.com/nuxt/movies
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  experimental: {
    viewTransition: true,
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:8001/api/v1',
    },
  },
})
