<script setup lang="ts">
import type { PropType } from 'vue'

import CardBox from '@/components/CardBox.vue'

type itemsType = {
  [key: string]: any
  id: string
}

defineProps({
  items: {
    type: Array as PropType<itemsType[]>,
    default: null,
  },
  headers: {
    type: Array as PropType<string[]>,
    default: null,
  },
})
</script>

<template>
  <card-box class="mb-6" has-table>
    <table>
      <thead>
        <tr>
          <th v-for="header in headers" :key="header.toString()">
            {{ header }}
          </th>
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
