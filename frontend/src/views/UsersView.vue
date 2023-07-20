<template>
  <layout-authenticated>
    <section-main>
      <section-title-line-with-button
        :icon="mdiTableBorder"
        title="Users"
        main
      ></section-title-line-with-button>
      <div class="grid grid-cols-1 lg:grid-cols-1 gap-6 mb-6">
        <table-card
          :items="users"
          :fields="userHeaders"
          pagination
          :total-rows="users.length"
          v-model="currentPage"
          :per-page="postsPerPage"
        />
      </div>
    </section-main>
  </layout-authenticated>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import LayoutAuthenticated from '@/layouts/LayoutAuthenticated.vue'
import SectionMain from '@/components/SectionMain.vue'

import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'

import { mdiTableBorder } from '@mdi/js'

import { usersApi } from '@/api/users'
import TableCard from '@/components/TableCard.vue'

interface Profile {
  id: string
  email: string
  isAdmin: boolean
  createDate: Date
}

const users = ref([] as Profile[])
const errors = ref(null)

const currentPage = ref(1)
const postsPerPage = ref(2)

const userHeaders = ref([
  { value: 'created_date', text: 'Created Date' },
  { value: 'email', text: 'Email' },
  { value: 'is_admin', text: 'Is Admin' },
])

async function getUsers(): Promise<Profile> {
  return await usersApi
    .getUsers()
    .then((res: Array<Profile>) => {
      return (users.value = res)
    })
    .catch((err) => {
      return (errors.value = err)
    })
}
onMounted(async () => {
  await getUsers()
})
</script>

<style scoped></style>
