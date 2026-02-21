/**
 * Simple toast/feedback state for API success and error messages.
 * Use with a small toast component or inline message in pages.
 */
export function useToast() {
  const message = ref<string | null>(null)
  const isError = ref(false)

  function show(msg: string, error = false) {
    message.value = msg
    isError.value = error
  }

  function success(msg: string) {
    show(msg, false)
  }

  function error(msg: string) {
    show(msg, true)
  }

  function clear() {
    message.value = null
    isError.value = false
  }

  return { message, isError, show, success, error, clear }
}
