<script setup lang="ts">
import { onMounted, ref } from "vue"

const props = withDefaults(
  defineProps<{
    type?: string
    placeholder?: string
    autofocus?: boolean
  }>(),
  {
    type: "text",
    placeholder: "",
    autofocus: false,
  },
)

const model = defineModel<string>()
const inputEl = ref<HTMLInputElement | null>(null)

onMounted(() => {
  if (props.autofocus && window.matchMedia("(pointer: fine)").matches) {
    inputEl.value?.focus()
  }
})
</script>

<template>
  <input
    ref="inputEl"
    :type="props.type"
    :placeholder="props.placeholder"
    :value="model"
    class="glass-field hairline box-border h-12 w-full rounded-input px-4 font-sans text-[15px] text-main outline-none transition-[border-color,box-shadow,background-color] duration-200 placeholder:text-second/80 hover:border-main/20 focus-glow"
    @input="model = ($event.target as HTMLInputElement).value"
  />
</template>
