<script setup lang="ts">
import NavIcon, { type IconName } from "@/components/nav-icon.vue"

withDefaults(
  defineProps<{
    type?: "button" | "submit" | "reset"
    variant?: "primary" | "ghost"
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
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    :class="[
      'inline-flex cursor-pointer items-center justify-center gap-2 transition-colors duration-150 disabled:cursor-not-allowed disabled:opacity-60',
      variant === 'primary'
        ? 'h-11 rounded-input bg-accent px-4 text-[15px] font-semibold text-bg hover:bg-accent-hover'
        : 'bg-transparent text-sm font-medium text-second hover:text-main',
    ]"
  >
    <NavIcon :name="icon" />
    <span v-if="!shortMode"><slot /></span>
  </button>
</template>
