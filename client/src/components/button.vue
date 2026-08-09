<script setup lang="ts">
withDefaults(
  defineProps<{
    type?: "button" | "submit" | "reset"
    variant?: "primary" | "ghost"
    disabled?: boolean
  }>(),
  {
    type: "button",
    variant: "primary",
    disabled: false,
  },
)
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    :class="[
      'cursor-pointer transition-colors duration-150 disabled:cursor-not-allowed disabled:opacity-60',
      variant === 'primary'
        ? 'h-11 rounded-input bg-accent text-[15px] font-semibold text-bg hover:bg-accent-hover'
        : 'bg-transparent text-sm font-medium text-second hover:text-main',
    ]"
  >
    <slot />
  </button>
</template>
