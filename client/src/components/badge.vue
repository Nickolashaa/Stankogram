<script setup lang="ts">
import { computed } from "vue"
import type { BadgeVariant } from "@/lib/badges"
import NavIcon, { type IconName } from "@/components/nav-icon.vue"

const props = defineProps<{
  variant: BadgeVariant
  label: string
}>()

const iconByVariant: Partial<Record<BadgeVariant, IconName>> = {
  developer: "code",
  "chat-admin": "crown",
  muted: "mute",
}

const colorClasses: Record<BadgeVariant, string> = {
  role: "bg-second/10 text-second",
  developer: "bg-accent/15 text-accent",
  "chat-admin": "bg-blue-500/10 text-blue-600 dark:text-blue-400",
  muted: "bg-red-500/10 text-red-600 dark:text-red-400",
}

const icon = computed(() => iconByVariant[props.variant])
</script>

<template>
  <span
    v-if="icon"
    class="inline-flex h-7 w-7 shrink-0 items-center justify-center rounded-full"
    :class="colorClasses[variant]"
    :title="label"
  >
    <NavIcon :name="icon" :size="16" />
  </span>
  <span
    v-else
    class="inline-flex shrink-0 items-center rounded-full px-2.5 py-0.5 text-xs font-medium whitespace-nowrap"
    :class="colorClasses[variant]"
  >
    {{ label }}
  </span>
</template>
