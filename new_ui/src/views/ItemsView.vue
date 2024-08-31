<script setup lang="ts">
import BaseCard from '@/components/bases/BaseCard.vue'
import BaseTable, { type TableFieldsI } from '@/components/bases/BaseTable.vue'
import { ref } from 'vue'
import type { Item } from '@/interfaces/Items'

const items = ref<Item[]>([])
const itemHeaders = ref<TableFieldsI[]>([{ text: 'Name', value: 'name' }])
const itemCount = ref(0)
const currentPage = ref(1)
const perPage = ref(20)
</script>

<template>
  <base-card>
    <base-table
      :items="items"
      :headers="itemHeaders"
      pagination
      :total-rows="itemCount"
      v-model="currentPage"
      :per-page="perPage"
    >
    </base-table>
  </base-card>
</template>

<style scoped></style>
