<script setup lang="ts" generic="T extends ItemType">
import type { PropType } from 'vue'

import type { TableFieldsI, ItemType } from '@/interfaces/Components'

import CardBox from '@/components/CardBox.vue'
import TableBase from '@/components/base-components/TableBase.vue'

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
  <card-box class="mb-6" has-table>
    <table-base :items="items" :fields="fields" />
  </card-box>
</template>
