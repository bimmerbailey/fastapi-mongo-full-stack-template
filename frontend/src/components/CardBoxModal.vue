<script setup lang="ts">
import { computed } from 'vue'
import { mdiClose } from '@mdi/js'
import BaseButton from '@/components/base-components/BaseButton.vue'
import BaseButtons from '@/components/base-components/BaseButtons.vue'
import CardBox from '@/components/CardBox.vue'
import OverlayLayer from '@/components/OverlayLayer.vue'
import CardBoxComponentTitle from '@/components/CardBoxComponentTitle.vue'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  button: {
    type: String,
    default: 'info',
  },
  buttonLabel: {
    type: String,
    default: 'Done',
  },
  hasCancel: Boolean,
  modelValue: {
    type: [String, Number, Boolean],
    default: null,
  },
  hasFooter: {
    type: Boolean,
    default: true,
    required: false,
  },
})

// const emit = defineEmits(['update:modelValue', 'cancel', 'confirm'])

const emit = defineEmits<{
  (e: 'update:modelValue', value: any): void
  (e: 'cancel'): void
  (e: 'confirm'): void
}>()

const value = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

const confirmCancel = (mode: any | null) => {
  value.value = false
  emit(mode)
}

const confirm = () => confirmCancel('confirm')

const cancel = () => confirmCancel('cancel')

window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && value.value) {
    cancel()
  }
})
</script>

<template>
  <OverlayLayer v-show="value" @overlay-click="cancel">
    <CardBox
      v-show="value"
      class="shadow-lg max-h-modal w-11/12 md:w-3/5 lg:w-2/5 xl:w-4/12 z-50"
      is-modal
    >
      <CardBoxComponentTitle :title="title">
        <BaseButton
          v-if="hasCancel"
          :icon="mdiClose"
          color="whiteDark"
          small
          rounded-full
          @click.prevent="cancel"
        />
      </CardBoxComponentTitle>

      <div class="space-y-3">
        <slot name="body" />
      </div>

      <template #footer v-if="hasFooter">
        <slot name="footer">
          <BaseButtons>
            <BaseButton :label="buttonLabel" :color="button" @click="confirm" />
            <BaseButton
              v-if="hasCancel"
              label="Cancel"
              :color="button"
              outline
              @click="cancel"
            />
          </BaseButtons>
        </slot>
      </template>
    </CardBox>
  </OverlayLayer>
</template>
