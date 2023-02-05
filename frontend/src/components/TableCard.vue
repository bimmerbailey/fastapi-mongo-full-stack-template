<script setup>
import CardBox from '@/components/CardBox.vue'

defineProps({
  items: {
    type: Array,
    default: null,
  },
  headers: {
    type: Array,
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
