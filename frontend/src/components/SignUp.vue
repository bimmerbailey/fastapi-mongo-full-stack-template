<template>
  <div>
    <form>
      <h3>Sign Up</h3>
      <b-form-group>
        <label>Full Name</label>
        <input type="text" class="form-control form-control-lg" />
      </b-form-group>
      <b-form-group>
        <label>Email address</label>
        <input type="email" class="form-control form-control-lg" />
      </b-form-group>
      <b-form-group>
        <label>Password</label>
        <input type="password" class="form-control form-control-lg" />
      </b-form-group>
      <button type="submit" class="btn btn-dark btn-lg btn-block">
        Sign Up
      </button>
      <p class="forgot-password text-right">
        Already registered
        <RouterLink :to="{ name: 'login' }">sign in?</RouterLink>
      </p>
    </form>
  </div>
</template>

<script lang="ts">
import { RouterLink } from 'vue-router'
import { defineComponent } from 'vue'

export default defineComponent({
  components: {
    RouterLink,
  },
})
</script>

<style scoped></style>
