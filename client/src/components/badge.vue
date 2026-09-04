<script setup lang="ts">
import { computed, ref } from "vue"
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

const badgeEl = ref<HTMLElement | null>(null)
const tooltipPosition = ref<{ top: number; left: number } | null>(null)

function showTooltip() {
  const rect = badgeEl.value?.getBoundingClientRect()
  if (!rect) {
    return
  }
  tooltipPosition.value = { top: rect.top, left: rect.left + rect.width / 2 }
}

function hideTooltip() {
  tooltipPosition.value = null
}
</script>

<template>
  <span
    v-if="icon"
    ref="badgeEl"
    class="inline-flex h-7 w-7 shrink-0 items-center justify-center rounded-full"
    :class="colorClasses[variant]"
    @mouseenter="showTooltip"
    @mouseleave="hideTooltip"
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

  <Teleport to="body">
    <span
      v-if="tooltipPosition"
      class="pointer-events-none fixed z-50 -translate-x-1/2 -translate-y-full rounded-input bg-main px-2 py-1 text-xs font-medium whitespace-nowrap text-bg shadow-card"
      :style="{ top: `${tooltipPosition.top - 6}px`, left: `${tooltipPosition.left}px` }"
    >
      {{ label }}
    </span>
  </Teleport>
</template>
