<script setup lang="ts">
import { useRouter } from 'vue-router'
import { mdiAccount, mdiAsterisk } from '@mdi/js'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'

import { ref } from 'vue'
import type { Ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import BaseButtons from '@/components/base-components/BaseButtons.vue'
import BaseButton from '@/components/base-components/BaseButton.vue'
import type { AxiosError } from 'axios'

const router = useRouter()
const store = useAuthStore()

const email: Ref<string | undefined> = ref(undefined)
const password: Ref<string | undefined> = ref(undefined)
const passwordCheck: Ref<string | undefined> = ref(undefined)
const error: Ref<AxiosError | string | undefined> = ref(undefined)

const emit = defineEmits(['signUpClose'])

const close = () => {
  error.value = undefined
  email.value = undefined
  password.value = undefined
  passwordCheck.value = undefined
  emit('signUpClose')
}

async function SignUp() {
  if (email.value && password.value) {
    if (password.value == passwordCheck.value) {
      return await store
        .createUser(email.value, password.value)
        .then(async () => {
          await router.push('/')
        })
        .catch((err) => {
          return (error.value = err)
        })
    } else {
      return (error.value = 'Passwords must match')
    }
  } else {
    return (error.value = 'Email and password are required')
  }
}
</script>

<template>
  <div>
    <FormField label="Email" help="Please enter your email">
      <FormControl
        v-model="email"
        :icon="mdiAccount"
        name="email"
        autocomplete="username"
      />
    </FormField>

    <FormField label="Password" help="Please enter your password">
      <FormControl
        v-model="password"
        :icon="mdiAsterisk"
        type="password"
        name="password"
        autocomplete="current-password"
      />
    </FormField>

    <FormField label="Confirm Password" help="Please re-enter your password">
      <FormControl
        v-model="passwordCheck"
        :icon="mdiAsterisk"
        type="password"
        name="confirm-password"
        autocomplete="current-password"
      />
    </FormField>
    <div v-if="error" class="text-rose-700 text-center mb-5 font-bold">
      {{ error }}
    </div>
    <BaseButtons class="justify-center">
      <BaseButton label="Sign Up" @click="SignUp" />
      <BaseButton label="Cancel" outline @click="close" />
    </BaseButtons>
  </div>
</template>

<style scoped></style>
