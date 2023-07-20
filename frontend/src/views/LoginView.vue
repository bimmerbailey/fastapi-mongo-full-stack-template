<template>
  <LayoutGuest>
    <card-box-modal title="Error" v-model="error" button="danger">{{
      error
    }}</card-box-modal>
    <card-box-modal
      title="Sign Up"
      v-model="signUpModal"
      button-label="Sign Up"
      :has-footer="false"
    >
      <template #body>
        <sign-up @sign-up-close="signUpModal = false" />
      </template>
    </card-box-modal>
    <SectionFullScreen v-slot="{ cardClass }" bg="purplePink">
      <CardBox :class="cardClass" is-form @submit.prevent>
        <FormField label="Login" help="Please enter your login">
          <FormControl
            v-model="email"
            :icon="mdiAccount"
            name="login"
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

        <template #footer>
          <BaseButtons class="justify-center">
            <BaseButton
              @click="Login"
              type="submit"
              color="info"
              label="Login"
            />
            <BaseButton
              color="info"
              outline
              label="Sign Up"
              @click="signUpModal = !signUpModal"
            />
          </BaseButtons>
        </template>
      </CardBox>
    </SectionFullScreen>
  </LayoutGuest>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router'
import { mdiAccount, mdiAsterisk } from '@mdi/js'
import SectionFullScreen from '@/components/SectionFullScreen.vue'
import CardBox from '@/components/CardBox.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import BaseButton from '@/components/base-components/BaseButton.vue'
import BaseButtons from '@/components/base-components/BaseButtons.vue'
import LayoutGuest from '@/layouts/LayoutGuest.vue'
import CardBoxModal from '@/components/CardBoxModal.vue'
import SignUp from '@/components/SignUp.vue'

import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const store = useAuthStore()

const email = ref()
const password = ref()
const error = ref()
const signUpModal = ref(false)

async function Login() {
  if (!email.value || !password.value) {
    return (error.value = 'Email and password required')
  }
  return await store
    .login(email.value, password.value)
    .then(async () => {
      return await router.push('/')
    })
    .catch((err) => {
      return (error.value = err.response.data.detail || err.message)
    })
}
</script>
