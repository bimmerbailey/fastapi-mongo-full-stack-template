<script setup lang="ts" generic="T extends ItemType">
import Pagination from '@/components/bases/BasePagination.vue'

export interface TableFieldsI {
  [key: string]: string

  text: string
  value: string
}

export type ItemType = Record<string, any>

defineProps<{
  items: T[]
  headers: TableFieldsI[]
  pagination?: boolean
  totalRows: number
  perPage: number
}>()

const value = defineModel<number>({ required: true })
</script>

<template>
  <table>
    <thead>
      <tr>
        <th v-for="field in headers" :key="field.value">
          {{ field.text }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in items" :key="item.id">
        <td v-for="field in headers" :key="`${item.id}_${field}`">
          <slot :name="`cell(${field.value})`" :value="item[field.value]" :item="item">
            {{ item[field.value] }}
          </slot>
        </td>
      </tr>
    </tbody>
  </table>
  <div class="text-center">
    <pagination v-if="pagination" :total-rows="totalRows" :per-page="perPage" v-model="value" />
  </div>
</template>

<style scoped></style>
