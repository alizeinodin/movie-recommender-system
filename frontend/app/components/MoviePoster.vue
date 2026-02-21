<template>
  <div class="absolute inset-0 w-full h-full">
    <img
      v-if="effectivePosterUrl"
      :src="effectivePosterUrl"
      :alt="title"
      class="w-full h-full object-cover"
      loading="lazy"
      @error="imageError = true"
    />
    <div
      v-else
      class="absolute inset-0 flex items-center justify-center text-white font-bold text-4xl select-none overflow-hidden"
      :style="posterStyle"
    >
      <span class="drop-shadow-md">{{ initial }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    movieId: number
    title: string
    posterUrl?: string | null
  }>(),
  { posterUrl: null }
)

const imageError = ref(false)
const effectivePosterUrl = computed(() => {
  const url = props.posterUrl?.trim()
  if (!url || imageError.value) return null
  return url
})

// Fallback: deterministic gradient from movie id
const hue = computed(() => (props.movieId * 137.508) % 360)
const posterStyle = computed(() => ({
  background: `linear-gradient(135deg, hsl(${hue.value}, 55%, 25%) 0%, hsl(${hue.value}, 45%, 15%) 100%)`,
}))

const initial = computed(() => {
  const t = props.title?.trim() || '?'
  const first = t[0].toUpperCase()
  if (t.length > 1 && /[a-zA-Z]/.test(t[1])) {
    const second = t[1].toUpperCase()
    if (first !== second) return first + second
  }
  return first
})
</script>
