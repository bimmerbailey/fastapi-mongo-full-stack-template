<script setup lang="ts" generic="T extends  ItemType">
import type { PropType } from 'vue'
import type { TableFieldsI, ItemType } from '@/interfaces/Components'

import Pagination from '@/components/PaginationComponent.vue'
import { computed } from 'vue'

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
  <table>
    <thead>
      <tr>
        <th v-for="field in fields" :key="field.value">
          {{ field.text }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in items" :key="item.id">
        <td v-for="field in fields" :key="`${item.id}_${field}`">
          <slot
            :name="`cell(${field.value})`"
            :value="item[field.value]"
            :item="item"
          >
            {{ item[field.value] }}
          </slot>
        </td>
      </tr>
    </tbody>
  </table>
  <div class="text-center">
    <pagination
      v-if="pagination"
      :total-rows="totalRows"
      :per-page="perPage"
      v-model="currentPage"
    />
  </div>
</template>

<style scoped></style>
