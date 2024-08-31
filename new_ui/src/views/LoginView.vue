<script setup lang="ts">
import BaseForm from '@/components/bases/BaseForm.vue'
import BaseInput from '@/components/bases/BaseInput.vue'
import BaseCard from '@/components/bases/BaseCard.vue'
</script>

<template>
  <base-card>
    <template #header>
      <h1>Login</h1>
    </template>
    <base-form>
      <base-input type="text" id="username" label="Username" />
      <base-input type="password" id="password" label="Password" />
    </base-form>
    <template #footer>
      <div class="px-4">
        <button
          type="submit"
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Login
        </button>
      </div>
    </template>
  </base-card>
</template>

<style scoped></style>
