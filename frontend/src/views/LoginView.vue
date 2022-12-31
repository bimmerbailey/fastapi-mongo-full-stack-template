<template>
  <b-card class="align-items-center px-5">
    <b-row class="justify-content-center" v-if="window === 'register'">
      <div class="align-items-center justify-content-center">
        <p class="text-center h1 fw-bold">Sign up</p>

        <b-form-group class="text-center">
          <b-row>
            <b-col>
              <div>
                <b-form-input
                  type="email"
                  v-model="email"
                  class="form-control"
                />
                <label class="form-label" for="form3Example3c"
                  >Your Email</label
                >
              </div>
            </b-col>
          </b-row>

          <b-row>
            <b-col>
              <div class="form-outline flex-fill mb-0">
                <b-form-input
                  type="password"
                  v-model="password"
                  class="form-control"
                />
                <label class="form-label" for="form3Example4c">Password</label>
              </div>
            </b-col>
          </b-row>

          <b-row>
            <b-col>
              <div class="form-outline flex-fill mb-0">
                <b-form-input
                  type="password"
                  v-model="passwordCheck"
                  class="form-control"
                />
                <label class="form-label" for="form3Example4cd"
                  >Repeat your password</label
                >
              </div>
            </b-col>
          </b-row>

          <b-row>
            <b-col>
              <div>
                <b-form-checkbox class="form-check-input" v-model="checked">
                  <label class="form-check-label">
                    I agree to the
                    <a href="#" class="d-inline">Terms of service</a>
                  </label>
                </b-form-checkbox>
              </div>
            </b-col>
          </b-row>

          <b-row class="justify-content-center">
            <b-col class="justify-content-center">
              <button
                @click="SignUp"
                type="button"
                class="btn btn-primary btn-lg"
                :disabled="!checked"
              >
                Register
              </button>
            </b-col>
          </b-row>
          <b-row>
            <b-col class="d-flex justify-content-center">
              Already have an account?
              <a
                class="text-decoration-underline d-inline pointer"
                @click="window = 'login'"
              >
                Login
              </a>
            </b-col>
          </b-row>
        </b-form-group>
      </div>
    </b-row>
    <b-row v-else-if="window === 'login'">
      <div class="align-items-center justify-content-center">
        <p class="text-center h1 fw-bold">Log In</p>
        <p class="text-center h5 fw-bold text-danger" v-if="error">
          Error: {{ errorMessage }}
        </p>

        <b-form-group class="text-center">
          <b-row>
            <b-col>
              <div class="form-outline flex-fill mb-0">
                <b-form-input
                  type="email"
                  v-model="email"
                  class="form-control"
                />
                <label class="form-label" for="form3Example3c"
                  >Your Email</label
                >
              </div>
            </b-col>
          </b-row>

          <b-row>
            <b-col>
              <div class="form-outline flex-fill mb-0">
                <b-form-input
                  type="password"
                  v-model="password"
                  class="form-control"
                />
                <label class="form-label">Password</label>
              </div>
            </b-col>
          </b-row>

          <b-row class="align-self-center">
            <b-col>
              <button
                @click="SignIn"
                type="button"
                class="btn btn-primary btn-lg"
              >
                Log In
              </button>
            </b-col>
          </b-row>
          <b-row class="my-2">
            <b-col>
              Forgot Your
              <a
                class="text-decoration-underline d-inline pointer"
                @click="window = 'forgot'"
              >
                Password?
              </a>
            </b-col>
          </b-row>
          <b-row class="my-2">
            <b-col>
              Don't have an account?
              <a
                class="text-decoration-underline d-inline pointer"
                @click="window = 'register'"
              >
                Register
              </a>
            </b-col>
          </b-row>
        </b-form-group>
      </div>
    </b-row>
    <b-row v-else-if="window === 'forgot'">
      <b-col>
        <ForgotPassword></ForgotPassword>
      </b-col>
    </b-row>
  </b-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import ForgotPassword from '@/components/ForgotPassword.vue'

const router = useRouter()
const store = useAuthStore()

const checked = ref(false)
const email = ref('')
const password = ref('')
const passwordCheck = ref('')
const error = ref(false)
const errorMessage = ref('')
const window = ref('login')

async function SignUp() {
  if (password.value == passwordCheck.value) {
    return await store
      .createUser(email.value, password.value)
      .then(async () => {
        await router.push('/')
      })
      .catch((err) => {
        error.value = true
        errorMessage.value = err.detail || err.message
      })
  } else {
    error.value = true
    errorMessage.value = 'Passwords must match'
  }
}

async function SignIn() {
  return await store
    .login(email.value, password.value)
    .then(async () => {
      await router.push('/')
    })
    .catch((err) => {
      error.value = true
      errorMessage.value = err.detail || err.message
    })
}
</script>

<style>
.pointer {
  cursor: pointer;
}
</style>
