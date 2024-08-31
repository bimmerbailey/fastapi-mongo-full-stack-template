<script setup lang="ts">
import { RouterView } from 'vue-router'
import { ref } from 'vue'

const currentYear = ref<number>(new Date().getFullYear())
</script>

<template>
  <div class="h-screen flex flex-col">
    <header class="flex p-4 bg-gray-200">FAVM App</header>
    <div class="flex flex-auto bg-gray-100 overflow-auto">
      <main class="grow bg-blue-500 place-content-center gap-2">
        <router-view />
      </main>
    </div>
    <footer class="flex p-4 bg-gray-200">
      <p class="text-center text-gray-500 text-xs">
        Copyright &copy;{{ currentYear }} Your Business. All rights reserved.
      </p>
    </footer>
  </div>
</template>

<style scoped></style>
