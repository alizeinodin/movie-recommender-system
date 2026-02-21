const STORAGE_KEY = 'moviebox_user_id'
const DEFAULT_USER_ID = 196

/** Shared user id across the app; persisted to localStorage so refresh keeps the same user and recommendations. */
export function usePersistedUser() {
  const route = useRoute()

  const userId = useState('moviebox_user_id', () => DEFAULT_USER_ID)

  function setUser(id: number) {
    const n = Math.max(1, Math.min(943, Number(id)))
    userId.value = n
    if (import.meta.client && typeof localStorage !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, String(n))
    }
  }

  onMounted(() => {
    if (import.meta.client && typeof localStorage !== 'undefined') {
      const q = route.query?.user_id
      if (q) {
        const n = Number(q)
        if (n >= 1 && n <= 943) {
          userId.value = n
          localStorage.setItem(STORAGE_KEY, String(n))
        }
      } else {
        const stored = localStorage.getItem(STORAGE_KEY)
        if (stored) {
          const n = Number(stored)
          if (n >= 1 && n <= 943) userId.value = n
        }
        // Sync URL so refresh keeps the same user
        navigateTo({ path: route.path, query: { ...route.query, user_id: String(userId.value) } }, { replace: true })
      }
    }
  })

  watch(userId, (id) => {
    if (import.meta.client && typeof localStorage !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, String(id))
    }
  })

  return { userId, setUser }
}
