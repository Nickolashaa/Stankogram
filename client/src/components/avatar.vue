<script setup lang="ts">
withDefaults(
  defineProps<{
    label: string
    size?: "sm" | "md" | "lg"
  }>(),
  {
    size: "md",
  },
)
</script>

<template>
  <span
    class="avatar-surface flex shrink-0 items-center justify-center rounded-full font-semibold text-accent"
    :class="{
      'h-9 w-9 text-xs': size === 'sm',
      'h-11 w-11 text-sm': size === 'md',
      'h-14 w-14 text-base': size === 'lg',
    }"
  >
    {{ label }}
  </span>
</template>
