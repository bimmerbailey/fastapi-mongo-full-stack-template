<script setup lang="ts">
import BaseIcon from '@/components/bases/BaseIcon.vue'
import { computed } from 'vue'

const props = defineProps<{
  icon?: string
  text?: number
  disabled?: boolean
}>()

const disableButton = computed(() => props.disabled ?? false)
</script>

<template>
  <button :disabled="disableButton">
    <base-icon v-if="icon" :icon="icon" />
    {{ text }}
  </button>
</template>

<style scoped></style>
