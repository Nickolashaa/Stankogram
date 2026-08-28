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
    v-model="model"
    class="box-border h-12 w-full rounded-input border-[1.5px] border-second/30 bg-bg px-4 font-sans text-[15px] text-main outline-none transition-colors duration-150 placeholder:text-second focus:border-accent"
  />
</template>
