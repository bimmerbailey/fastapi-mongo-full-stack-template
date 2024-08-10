<script setup lang="ts">
import { useSlots, computed } from 'vue'

const slots = useSlots()

const hasFooter = computed((): boolean => {
  return !!slots.footer
})
</script>

<template>
  <div class="max-w-md mx-auto space-y-6">
    <slot name="header" />
    <div class="flex-1 p-2">
      <slot />
    </div>
    <footer class="p-2" v-if="hasFooter">
      <slot name="footer" />
    </footer>
  </div>
</template>

<style scoped></style>
