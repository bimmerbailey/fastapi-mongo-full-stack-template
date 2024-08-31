<script setup lang="ts">
const modelValue = defineModel<any>()
const props = defineProps<{
  type: 'number' | 'password' | 'email' | 'text'
  id: string
  label?: string
  placeholder?: string
}>()
</script>

<template>
  <div class="m-2">
    <label v-if="label" :for="id">
      {{ label }}
    </label>
    <input
      class="shadow appearance-none border rounded w-full p-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
      v-model="modelValue"
      :type="type"
      :id="id"
      :placeholder="placeholder"
    />
  </div>
</template>

<style scoped></style>
