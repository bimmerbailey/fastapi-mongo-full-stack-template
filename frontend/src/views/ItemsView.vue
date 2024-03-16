<template>
  <layout-authenticated>
    <section-main>
      <section-title-line-with-button
        :icon="mdiTableBorder"
        title="Items"
        main
      ></section-title-line-with-button>
      <card-box has-table>
        <base-table
          :items="products"
          :fields="headers"
          pagination
          :total-rows="itemCount"
          v-model="currentPage"
          :per-page="perPage"
        >
        </base-table>
      </card-box>
    </section-main>
  </layout-authenticated>
</template>

<script lang="ts" setup>
import { onMounted, ref, watch } from 'vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionMain from '@/components/SectionMain.vue'
import type { PaginatedReturn, Item } from '@/interfaces/Items'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'

import { mdiTableBorder } from '@mdi/js'

import { itemApi } from '@/api/items'
import CardBox from '@/components/CardBox.vue'
import BaseTable from '@/components/base-components/BaseTable.vue'

const products = ref([] as Item[])
const errors = ref(null)

const currentPage = ref(1)
const perPage = ref(20)
const searchTerm = ref<string | undefined>(undefined)
const itemCount = ref<number>(0)

const headers = ref([
  { value: 'name', text: 'Name' },
  { value: 'description', text: 'Description' },
  { value: 'quantity', text: 'Quantity' },
  { value: 'cost', text: 'Cost' },
])

async function getItems(): Promise<null> {
  const offset = (currentPage.value - 1) * perPage.value
  return await itemApi
    .getItems(searchTerm.value, perPage.value, offset)
    .then((res: PaginatedReturn) => {
      console.log(res)
      itemCount.value = res.count
      products.value = res.items
    })
    .catch((err) => {
      return (errors.value = err)
    })
}

watch(currentPage, async () => {
  return await getItems()
})

onMounted(async () => {
  await getItems()
})
</script>

<style scoped></style>
