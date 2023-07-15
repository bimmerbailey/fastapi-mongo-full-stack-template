<script setup lang="ts">
import { toRefs } from 'vue'
import {
  mdiChevronLeft,
  mdiChevronRight,
  mdiChevronDoubleLeft,
  mdiChevronDoubleRight,
} from '@mdi/js'
import BaseIcon from '@/components/base-components/BaseIcon.vue'
import BaseButton from '@/components/base-components/BaseButton.vue'

const props = defineProps({
  totalRows: {
    type: Number,
    default: null,
  },
  perPage: {
    type: Number,
    required: true,
    default: null,
  },
  modelValue: {
    type: Number,
    required: true,
  },
})

const { perPage, totalRows, modelValue } = toRefs(props)

const emit = defineEmits<{
  'update:modelValue': [page: number]
  pageUpdate: [page: number]
}>()

function sendEmit(value: number) {
  emit('update:modelValue', value)
  emit('pageUpdate', value)
}

function prevPage() {
  if (modelValue.value <= 1) return
  sendEmit(modelValue.value - 1)
}
function nextPage() {
  if (modelValue.value >= Math.floor(totalRows.value / perPage.value)) return
  sendEmit(modelValue.value + 1)
}
</script>

<template>
  <div class="inline-flex items-center justify-center gap-3">
    <base-button @click="sendEmit(1)" color="transparent" small>
      <slot name="prev-button">
        <base-icon :path="mdiChevronDoubleLeft" size="24" />
      </slot>
    </base-button>
    <base-button @click="prevPage" color="transparent" small>
      <slot name="prev-button">
        <base-icon :path="mdiChevronLeft" size="24" />
      </slot>
    </base-button>
    <p class="text-xs">
      {{ modelValue }}
      <span class="mx-0.25">/</span>
      {{ Math.floor(totalRows / perPage) }}
    </p>

    <base-button @click="nextPage" color="transparent" small>
      <slot name="prev-button">
        <base-icon :path="mdiChevronRight" size="24" />
      </slot>
    </base-button>
    <base-button
      @click="sendEmit(Math.floor(totalRows / perPage))"
      color="transparent"
      small
    >
      <slot name="prev-button">
        <base-icon :path="mdiChevronDoubleRight" size="24" />
      </slot>
    </base-button>
  </div>
</template>

<style scoped></style>
