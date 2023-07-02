<script setup lang="ts" generic="T extends  ItemType">
import type { PropType } from 'vue'
import type { TableFieldsI, ItemType } from '@/interfaces/Components'

defineProps({
  items: {
    type: Array as PropType<T[]>,
  },
  fields: {
    type: Array as PropType<TableFieldsI[]>,
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
</template>

<style scoped></style>
