<script setup lang="ts" generic="T extends string">
const model = defineModel<T>()
</script>

<template>
  <select
    v-model="model"
    class="box-border h-12 w-full rounded-input border-[1.5px] border-second/30 bg-bg px-4 font-sans text-[15px] text-main outline-none transition-colors duration-150 focus:border-accent"
  >
    <slot />
  </select>
</template>
