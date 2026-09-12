<script setup lang="ts" generic="T extends string">
const model = defineModel<T>()
</script>

<template>
  <select
    v-model="model"
    class="glass-field hairline box-border h-12 w-full cursor-pointer rounded-input px-4 font-sans text-[15px] text-main outline-none transition-[border-color,box-shadow,background-color] duration-200 hover:border-main/20 focus-glow"
  >
    <slot />
  </select>
</template>
