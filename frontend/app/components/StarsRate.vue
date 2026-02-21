<template>
  <div class="flex items-center gap-1" role="group" aria-label="Rate from 1 to 5 stars">
    <button
      v-for="star in 5"
      :key="star"
      type="button"
      class="p-0.5 text-2xl leading-none transition-transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-[#111] rounded"
      :class="star <= (modelValue ?? 0) ? 'text-yellow-400' : 'text-gray-600 hover:text-gray-500'"
      :aria-label="`${star} star${star > 1 ? 's' : ''}`"
      @click="emit('update:modelValue', star)"
    >
      ★
    </button>
    <span v-if="modelValue" class="ml-2 text-sm text-gray-400">{{ modelValue }}/5</span>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue?: number
}>()
const emit = defineEmits<{
  'update:modelValue': [value: number]
}>()
</script>
