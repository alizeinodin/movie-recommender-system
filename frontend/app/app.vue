<template>
  <div class="min-h-screen bg-[#111] text-white">
    <NuxtLoadingIndicator color="#e50914" :height="3" />
    <NuxtRouteAnnouncer />
    <NuxtPage />
  </div>
</template>

<script setup lang="ts">
useHead({
  htmlAttrs: { lang: 'en' },
  charset: 'utf-8',
  title: 'MovieBox',
  titleTemplate: (title) => (title !== 'MovieBox' ? `${title} · MovieBox` : title),
  meta: [
    { name: 'description', content: 'Movie recommender with deep learning (NCF) – browse and rate movies.' },
    { name: 'theme-color', content: '#111' },
  ],
  link: [{ rel: 'preconnect', href: 'https://fonts.googleapis.com' }, { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }, { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Serif+Display:ital@0;1&display=swap' }],
})
</script>

<style>
html, body, #__nuxt {
  height: 100%;
  margin: 0;
  padding: 0;
  color-scheme: dark;
  font-family: 'DM Sans', system-ui, sans-serif;
}
</style>
