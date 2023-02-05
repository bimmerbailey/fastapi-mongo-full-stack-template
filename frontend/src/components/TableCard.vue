<script lang="ts" setup>
import type { PropType } from 'vue'
import CardBox from '@/components/CardBox.vue'

interface ItemsI {
  [index: string]: string
  id: string
}

defineProps({
  items: {
    type: Array as PropType<Array<ItemsI>>,
    default: null,
  },
  headers: {
    type: Array as PropType<Array<string>>,
    default: null,
  },
})
</script>
Ï
<template>
  <card-box class="mb-6" has-table>
    <table>
      <thead>
        <tr>
          <th v-for="header in headers" :key="header">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td v-for="header in headers" :key="`${item.id}_${header}`">
            {{ item[header.toLowerCase()] }}
          </td>
        </tr>
      </tbody>
    </table>
  </card-box>
</template>
