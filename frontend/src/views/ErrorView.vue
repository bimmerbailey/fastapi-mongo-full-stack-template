<template>
  <LayoutGuest>
    <SectionFullScreen v-slot="{ cardClass }" bg="pinkRed">
      <CardBox :class="cardClass">
        <div class="space-y-3">
          <h1 class="text-2xl">Unhandled exception</h1>
          <p>An Error Occurred</p>
        </div>
        <template #footer>
          <BaseButtons>
            <BaseButton label="Done" to="/" color="danger" />
          </BaseButtons>
        </template>
      </CardBox>
    </SectionFullScreen>
  </LayoutGuest>
</template>

<script lang="ts" setup>
import SectionFullScreen from '@/components/SectionFullScreen.vue'
import CardBox from '@/components/CardBox.vue'
import BaseButton from '@/components/base-components/BaseButton.vue'
import BaseButtons from '@/components/base-components/BaseButtons.vue'
import LayoutGuest from '@/layouts/LayoutGuest.vue'
</script>
