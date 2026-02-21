<template>
  <section class="mb-14">
    <div v-if="!hideHeader" class="flex items-center justify-between mb-4">
      <div>
        <h2 class="text-2xl font-bold tracking-tight text-white">
          {{ title }}
        </h2>
        <p v-if="subtitle" class="text-gray-400 text-sm mt-1">{{ subtitle }}</p>
      </div>
      <div v-if="!hideNav" class="flex gap-2">
        <button
          type="button"
          class="p-2.5 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 transition-colors text-white font-medium"
          aria-label="Scroll left"
          @click="scrollLeft"
        >
          ‹
        </button>
        <button
          type="button"
          class="p-2.5 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 transition-colors text-white font-medium"
          aria-label="Scroll right"
          @click="scrollRight"
        >
          ›
        </button>
      </div>
    </div>
    <div
      ref="scrollEl"
      class="flex gap-4 overflow-x-auto overflow-y-hidden pb-4 -mx-1 scroll-smooth scrollbar-hide"
    >
      <slot />
    </div>
  </section>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    title?: string
    subtitle?: string
    hideNav?: boolean
    hideHeader?: boolean
  }>(),
  { title: '', subtitle: '', hideNav: false, hideHeader: false }
)

const scrollEl = ref<HTMLElement | null>(null)

function scrollLeft() {
  scrollEl.value?.scrollBy({ left: -window.innerWidth * 0.8, behavior: 'smooth' })
}

function scrollRight() {
  scrollEl.value?.scrollBy({ left: window.innerWidth * 0.8, behavior: 'smooth' })
}
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
