<script setup lang="ts">
import {
  mdiChevronLeft,
  mdiChevronRight,
  mdiChevronDoubleLeft,
  mdiChevronDoubleRight
} from '@mdi/js'
import BaseIcon from '@/components/bases/BaseIcon.vue'
import BaseButton from '@/components/bases/BaseButton.vue'

const props = defineProps<{
  totalRows: number
  perPage: number
}>()

const modelValue = defineModel<number>({ required: true })

function prevPage() {
  if (modelValue.value <= 1) return
  modelValue.value = -1
}

function nextPage() {
  if (modelValue.value >= Math.ceil(props.totalRows / props.perPage)) return
  modelValue.value += 1
}
</script>

<template>
  <div class="inline-flex items-center justify-center gap-3">
    <base-button @click="modelValue = 1" color="transparent">
      <slot name="prev-button">
        <base-icon :icon="mdiChevronDoubleLeft" size="24" />
      </slot>
    </base-button>
    <base-button @click="prevPage" color="transparent">
      <slot name="prev-button">
        <base-icon :icon="mdiChevronLeft" size="24" />
      </slot>
    </base-button>
    <p class="text-xs">
      {{ modelValue }}
      <span class="mx-0.25">/</span>
      {{ Math.floor(totalRows / perPage) }}
    </p>

    <base-button @click="nextPage" color="transparent">
      <slot name="prev-button">
        <base-icon :icon="mdiChevronRight" size="24" />
      </slot>
    </base-button>
    <base-button @click="modelValue = Math.floor(totalRows / perPage)" color="transparent">
      <slot name="prev-button">
        <base-icon :icon="mdiChevronDoubleRight" size="24" />
      </slot>
    </base-button>
  </div>
</template>

<style scoped></style>
