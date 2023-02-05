<script setup>
import { useMainStore } from '@/stores/main'
// import {useAuthStore} from '@/stores/auth'
import UserAvatar from '@/components/UserAvatar.vue'

const mainStore = useMainStore()
// const authStore = useAuthStore()
</script>

<template>
  <UserAvatar :username="mainStore.userName" :avatar="mainStore.userAvatar">
    <slot />
  </UserAvatar>
</template>
