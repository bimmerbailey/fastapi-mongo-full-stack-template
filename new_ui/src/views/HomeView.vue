<script setup lang="ts">
import LoginView from '@/views/LoginView.vue'
import BaseCard from '@/components/bases/BaseCard.vue'
</script>

<template>
  <div class="grid grid-cols-1 gap-6 lg:grid-cols-2 mb-6">
    <login-view />
    <base-card>
      <div class="text-center">Here we see another card</div>
    </base-card>
  </div>
</template>
