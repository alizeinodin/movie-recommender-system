<template>
  <div class="min-h-screen bg-[#111] text-white flex flex-col items-center justify-center px-6">
    <h1 class="text-4xl font-bold font-serif text-primary mb-4">Something went wrong</h1>
    <p class="text-gray-400 text-center max-w-md mb-8">
      {{ error?.message ?? 'An unexpected error occurred. Please try again.' }}
    </p>
    <NuxtLink
      to="/"
      class="px-6 py-3 rounded-lg bg-primary hover:bg-red-600 text-white font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-[#111]"
    >
      Back to home
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  error: { message?: string; statusCode?: number } | null
}>()
</script>
