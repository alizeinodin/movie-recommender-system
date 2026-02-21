<template>
  <header
    class="fixed top-0 left-0 right-0 z-50 transition-all duration-300"
    :class="scrolled ? 'bg-black/90 backdrop-blur-md shadow-lg shadow-black/20' : 'bg-gradient-to-b from-black/80 to-transparent'"
  >
    <nav class="flex items-center justify-between px-4 sm:px-6 lg:px-8 py-4 max-w-[1920px] mx-auto">
      <NuxtLink
        to="/"
        class="flex items-center gap-3 text-white hover:opacity-90 transition-opacity focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-black rounded-lg"
        aria-label="MovieBox home"
      >
        <span class="text-2xl font-bold font-serif tracking-tight">MovieBox</span>
        <span class="hidden sm:inline text-gray-400 text-sm font-normal font-sans">Recommender</span>
      </NuxtLink>

      <div class="flex items-center gap-4">
        <NuxtLink
          to="/"
          class="text-sm font-medium text-gray-300 hover:text-white transition-colors hidden sm:inline"
        >
          Home
        </NuxtLink>

        <div class="relative" ref="dropdownRef">
          <button
            type="button"
            :aria-expanded="open"
            aria-haspopup="listbox"
            aria-label="Select user profile"
            class="flex items-center gap-2 min-w-[140px] sm:min-w-[170px] rounded-xl px-4 py-2.5 text-left text-sm font-medium bg-white/10 text-white border border-white/20 hover:bg-white/15 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
            @click="open = !open"
          >
            <span class="text-gray-400 text-xs uppercase tracking-wider hidden sm:inline">Profile</span>
            <span class="flex-1 font-semibold">User {{ currentUserId }}</span>
            <span class="text-gray-500 text-xs" aria-hidden="true">{{ open ? '▲' : '▼' }}</span>
          </button>

          <Transition
            enter-active-class="transition ease-out duration-200"
            enter-from-class="opacity-0 translate-y-2"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 translate-y-2"
          >
            <ul
              v-show="open"
              role="listbox"
              class="absolute right-0 mt-2 w-60 rounded-xl bg-gray-900/95 backdrop-blur border border-gray-700 shadow-2xl shadow-black/50 py-2 max-h-80 overflow-auto"
              :aria-label="`User ID list, current: ${currentUserId}`"
            >
              <li
                v-for="u in userOptions"
                :key="u"
                role="option"
                :aria-selected="currentUserId === u"
                class="px-4 py-3 cursor-pointer text-sm transition-colors"
                :class="currentUserId === u ? 'bg-primary/25 text-white font-medium' : 'text-gray-200 hover:bg-white/10 hover:text-white'"
                @click="selectUser(u)"
              >
                <span class="font-medium text-white">User {{ u }}</span>
                <span class="text-gray-500 text-xs ml-2">ID {{ u }}</span>
              </li>
            </ul>
          </Transition>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
const userOptions = [1, 2, 3, 10, 42, 100, 196, 300, 500]
const route = useRoute()
const { userId: currentUserId, setUser } = usePersistedUser()
const open = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)
const scrolled = ref(false)

function onScroll() {
  scrolled.value = typeof window !== 'undefined' && window.scrollY > 20
}

function selectUser(id: number) {
  currentUserId.value = id
  setUser(id)
  open.value = false
  navigateTo({ path: route.path, query: { ...route.query, user_id: String(id) } }, { replace: true })
}

watch(currentUserId, (id) => {
  setUser(id)
  navigateTo({ path: route.path, query: { ...route.query, user_id: String(id) } }, { replace: true })
})

onMounted(() => {
  const q = route.query?.user_id
  if (q) currentUserId.value = Number(q) || 196
  if (typeof window !== 'undefined') {
    window.addEventListener('scroll', onScroll, { passive: true })
    onScroll()
  }
  const close = (e: MouseEvent) => {
    if (dropdownRef.value && !dropdownRef.value.contains(e.target as Node)) open.value = false
  }
  document.addEventListener('click', close)
  onUnmounted(() => {
    document.removeEventListener('click', close)
    if (typeof window !== 'undefined') window.removeEventListener('scroll', onScroll)
  })
})
</script>
