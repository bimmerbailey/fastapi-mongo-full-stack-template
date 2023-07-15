<script setup lang="ts">
import BaseIcon from '@/components/base-components/BaseIcon.vue'

defineProps({
  label: {
    type: String,
    required: true,
  },
  icon: {
    type: String,
    default: null,
  },
  small: Boolean,
})
</script>

<template>
  <div
    class="inline-flex items-center capitalize leading-none"
    :class="[small ? 'text-xs' : 'text-sm']"
  >
    <BaseIcon
      v-if="icon"
      :path="icon"
      h="h-4"
      w="w-4"
      :class="small ? 'mr-1' : 'mr-2'"
      :size="small ? 14 : undefined"
    />
    <span>{{ label }}</span>
  </div>
</template>
