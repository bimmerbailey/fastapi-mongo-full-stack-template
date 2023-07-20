<script setup lang="ts" generic="T extends ItemType">
import { type PropType, computed } from 'vue'

import type { TableFieldsI, ItemType } from '@/interfaces/Components'

import CardBox from '@/components/CardBox.vue'
import BaseTable from '@/components/base-components/BaseTable.vue'

const props = defineProps({
  items: {
    type: Array as PropType<T[]>,
  },
  fields: {
    type: Array as PropType<TableFieldsI[]>,
  },
  pagination: {
    type: Boolean,
    default: false,
  },
  totalRows: {
    type: Number,
  },
  perPage: {
    type: Number,
  },
  modelValue: {
    type: Number,
    required: false,
    default: 1,
  },
})

const emit = defineEmits<{
  'update:modelValue': [page: number]
}>()

const currentPage = computed({
  get: () => {
    return props.modelValue
  },
  set: (value: number) => {
    emit('update:modelValue', value)
  },
})
</script>

<template>
  <card-box class="mb-6" has-table>
    <base-table
      :items="items"
      :fields="fields"
      :pagination="pagination"
      :total-rows="totalRows"
      :per-page="perPage"
      v-model="currentPage"
    />
  </card-box>
</template>
