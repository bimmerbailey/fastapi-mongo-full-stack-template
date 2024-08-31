<script setup lang="ts">
import BaseCard from '@/components/bases/BaseCard.vue'
import BaseTable from '@/components/bases/BaseTable.vue'
import { ref } from 'vue'

const items = ref([])
const itemHeaders = ref([])
const itemCount = ref(0)
</script>

<template>
  <base-card>
    <base-table :items="items" :headers="itemHeaders" v-model="itemCount">
    </base-table>
  </base-card>
</template>

<style scoped></style>
