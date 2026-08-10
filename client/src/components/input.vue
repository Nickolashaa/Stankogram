<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    type?: string
    placeholder?: string
  }>(),
  {
    type: "text",
    placeholder: "",
  },
)

const model = defineModel<string>()
</script>

<template>
  <input
    :type="props.type"
    :placeholder="props.placeholder"
    v-model="model"
    class="box-border h-12 w-full rounded-input border-[1.5px] border-second/30 bg-bg px-4 font-sans text-[15px] text-main outline-none transition-colors duration-150 placeholder:text-second focus:border-accent"
  />
</template>
