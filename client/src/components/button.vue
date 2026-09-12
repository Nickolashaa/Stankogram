<script setup lang="ts">
import { computed } from "vue"
import NavIcon, { type IconName } from "@/components/nav-icon.vue"

const props = withDefaults(
  defineProps<{
    type?: "button" | "submit" | "reset"
    variant?: "primary" | "ghost" | "soft" | "danger"
    disabled?: boolean
    icon: IconName
    shortMode?: boolean
  }>(),
  {
    type: "button",
    variant: "primary",
    disabled: false,
    shortMode: true,
  },
)

const shapeClasses = computed(() => {
  if (props.variant === "primary" || props.variant === "soft" || props.variant === "danger") {
    return props.shortMode ? "h-11 w-11 rounded-input" : "h-11 rounded-input px-5 text-[15px]"
  }
  return props.shortMode ? "h-10 w-10 rounded-full" : "h-11 rounded-input px-4 text-sm"
})

const toneClasses = computed(() => {
  switch (props.variant) {
    case "primary":
      return "accent-surface glow-accent font-semibold text-bg hover:brightness-110"
    case "soft":
      return "bg-accent/12 font-semibold text-accent hover:bg-accent/20"
    case "danger":
      return "bg-red-500/12 font-semibold text-red-600 hover:bg-red-500/20 dark:text-red-400"
    default:
      return "font-medium text-second hover:bg-main/6 hover:text-main"
  }
})
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    class="press focus-ring inline-flex cursor-pointer items-center justify-center gap-2 disabled:cursor-not-allowed disabled:opacity-50 disabled:shadow-none"
    :class="[shapeClasses, toneClasses]"
  >
    <NavIcon :name="icon" :size="variant === 'primary' ? 19 : 18" />
    <span v-if="!shortMode"><slot /></span>
  </button>
</template>
