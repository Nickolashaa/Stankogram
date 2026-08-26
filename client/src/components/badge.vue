<script setup lang="ts">
import type { BadgeVariant } from "@/lib/badges"

defineProps<{
  variant: BadgeVariant
}>()

const variantClasses: Record<BadgeVariant, string> = {
  role: "bg-second/10 text-second",
  developer: "bg-accent/15 text-accent",
  "chat-admin": "bg-blue-500/10 text-blue-600 dark:text-blue-400",
  muted: "bg-red-500/10 text-red-600 dark:text-red-400",
}
</script>

<template>
  <span
    class="inline-flex shrink-0 items-center rounded-full px-2.5 py-0.5 text-xs font-medium whitespace-nowrap"
    :class="variantClasses[variant]"
  >
    <slot />
  </span>
</template>
