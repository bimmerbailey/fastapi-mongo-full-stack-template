<template>
  <div class="vue-template">
    <form>
      <p class="text-center h1 fw-bold">Forgot Password</p>
      <b-form-group>
        <b-form-input type="email" v-model="email" class="form-control" />
        <label class="form-label">Your Email</label>
      </b-form-group>
      <button
        type="button"
        class="btn btn-primary btn-lg"
        @click="sendResetRequest"
      >
        Reset password
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { AuthApi } from '@/api'
const router = useRouter()

const email = ref('')
const error = ref('')

async function sendResetRequest() {
  return await AuthApi.forgotPassword(email.value)
    .then(async () => {
      await router.replace('/')
    })
    .catch((err) => {
      error.value = err.detail
    })
}
</script>

<style scoped></style>
