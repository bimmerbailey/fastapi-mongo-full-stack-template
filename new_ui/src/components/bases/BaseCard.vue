<script setup lang="ts">
import { useSlots, computed } from 'vue'

const slots = useSlots()

const hasFooter = computed((): boolean => {
  return !!slots.footer
})
</script>

<template>
  <div class="w-full max-w-lg px-10 py-8 mx-auto my-4 bg-amber-300 rounded-lg shadow-xl">
    <div class="max-w-md mx-auto space-y-6">
      <slot name="header" />
      <div class="flex-1 p-2">
        <slot />
      </div>
      <footer v-if="hasFooter">
        <slot name="footer" />
      </footer>
    </div>
  </div>
</template>

<style scoped></style>
