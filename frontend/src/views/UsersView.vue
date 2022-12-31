<template>
  <div>
    <b-row>
      <b-col>
        <b-button @click="submitButton" class="float-start"
          >View Users</b-button
        >
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <b-list-group>
          <b-list-group-item v-for="user in users" :key="user.id">
            {{ user }}
          </b-list-group-item>
        </b-list-group>
      </b-col>
    </b-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { AuthApi } from '@/api'

interface Profile {
  id: string
  email: string
  isAdmin: boolean
  createDate: Date
}

const users = ref([] as Profile[])
const store = useAuthStore()
const errors = ref(null)

function submitButton() {
  AuthApi.getUsers(store.authState.AccessToken)
    .then((res) => {
      if (res.ok) {
        return res.json()
      }
    })
    .then((res: Profile[]) => {
      users.value = res
    })
    .catch((err) => {
      errors.value = err
      console.log(err)
    })
}
</script>

<style scoped></style>
