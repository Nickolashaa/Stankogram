<script setup lang="ts">
withDefaults(
  defineProps<{
    label: string
    size?: "sm" | "md" | "lg"
    online?: boolean
  }>(),
  {
    size: "md",
    online: false,
  },
)
</script>

<template>
  <span
    class="avatar-surface relative flex shrink-0 items-center justify-center rounded-full font-semibold text-accent"
    :class="{
      'h-9 w-9 text-xs': size === 'sm',
      'h-11 w-11 text-sm': size === 'md',
      'h-14 w-14 text-base': size === 'lg',
    }"
  >
    {{ label }}
    <span
      v-if="online"
      class="absolute right-0 bottom-0 rounded-full bg-green-500 ring-2 ring-card"
      :class="{
        'h-2.5 w-2.5': size === 'sm',
        'h-3 w-3': size === 'md',
        'h-3.5 w-3.5': size === 'lg',
      }"
    />
  </span>
</template>
