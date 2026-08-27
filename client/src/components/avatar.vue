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
    class="flex shrink-0 items-center justify-center rounded-full bg-accent/15 font-semibold text-accent"
    :class="{
      'h-8 w-8 text-xs': size === 'sm',
      'h-10 w-10 text-sm': size === 'md',
      'h-12 w-12 text-[15px]': size === 'lg',
    }"
  >
    {{ label }}
  </span>
</template>
