<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  icon: string
  size?: string | number
}>()

const iconSize = computed(() => props.size ?? 16)
</script>

<template>
  <span>
    <svg viewBox="0 0 24 24" :width="iconSize" :height="iconSize" class="inline-block">
      <path fill="currentColor" :d="icon" />
    </svg>
  </span>
</template>
