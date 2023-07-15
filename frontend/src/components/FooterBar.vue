<script setup lang="ts">
import { containerMaxW } from '@/styles/config'
import BaseLevel from '@/components/base-components/BaseLevel.vue'
import { businessInfo } from '@/business'

const year = new Date().getFullYear()
</script>

<template>
  <footer class="py-2 px-6" :class="containerMaxW">
    <BaseLevel>
      <div class="text-center md:text-left">
        <b
          >&copy;{{ year }},
          <a :href="businessInfo.website" target="_blank">{{
            businessInfo.name
          }}</a>
        </b>
        <slot />
      </div>
      <div class="md:py-2">
        <img
          :src="businessInfo.logo"
          :alt="businessInfo.name"
          class="w-auto h-12 md:h-10"
        />
      </div>
    </BaseLevel>
  </footer>
</template>
