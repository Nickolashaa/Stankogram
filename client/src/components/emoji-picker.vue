<script setup lang="ts">
import { computed, ref, watch } from "vue"
import { EMOJI_GROUPS } from "@/lib/emoji"

const RECENT_STORAGE_KEY = "stankogram:recent-emoji"
const RECENT_LIMIT = 24

const props = defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  close: []
  select: [emoji: string]
}>()

function readRecent(): string[] {
  try {
    const raw = localStorage.getItem(RECENT_STORAGE_KEY)
    if (raw === null) {
      return []
    }
    const parsed: unknown = JSON.parse(raw)
    if (!Array.isArray(parsed)) {
      return []
    }
    return parsed.filter((item): item is string => typeof item === "string")
  } catch {
    return []
  }
}

const recent = ref<string[]>(readRecent())
const activeGroupId = ref(EMOJI_GROUPS[0]?.id ?? "")

const tabs = computed(() =>
  recent.value.length > 0
    ? [{ id: "recent", label: "Недавние", icon: "🕘" }, ...EMOJI_GROUPS]
    : EMOJI_GROUPS,
)

const visibleEmojis = computed(() => {
  if (activeGroupId.value === "recent") {
    return recent.value
  }
  return EMOJI_GROUPS.find((group) => group.id === activeGroupId.value)?.emojis ?? []
})

watch(
  () => props.open,
  (isOpen) => {
    if (!isOpen) {
      return
    }
    recent.value = readRecent()
    activeGroupId.value = recent.value.length > 0 ? "recent" : (EMOJI_GROUPS[0]?.id ?? "")
  },
)

function rememberEmoji(emoji: string) {
  const next = [emoji, ...recent.value.filter((item) => item !== emoji)].slice(0, RECENT_LIMIT)
  recent.value = next
  try {
    localStorage.setItem(RECENT_STORAGE_KEY, JSON.stringify(next))
  } catch {
    return
  }
}

function handleSelect(emoji: string) {
  rememberEmoji(emoji)
  emit("select", emoji)
}
</script>

<template>
  <div v-if="open" class="fixed inset-0 z-40" @click="emit('close')" />

  <div
    v-if="open"
    class="absolute right-0 bottom-full z-50 mb-2 flex w-full max-w-sm animate-appear flex-col overflow-hidden rounded-card border-[1.5px] border-second/15 bg-card shadow-card"
  >
    <div class="flex shrink-0 gap-0.5 overflow-x-auto border-b border-second/15 px-2 py-2">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        type="button"
        class="flex h-8 w-8 shrink-0 cursor-pointer items-center justify-center rounded-input text-base transition-colors duration-150"
        :class="activeGroupId === tab.id ? 'bg-accent/15' : 'hover:bg-accent/5'"
        :title="tab.label"
        :aria-label="tab.label"
        @click="activeGroupId = tab.id"
      >
        {{ tab.icon }}
      </button>
    </div>

    <div class="grid max-h-56 grid-cols-8 gap-0.5 overflow-y-auto p-2">
      <button
        v-for="(emoji, index) in visibleEmojis"
        :key="`${emoji}-${index}`"
        type="button"
        class="flex h-9 cursor-pointer items-center justify-center rounded-input text-xl leading-none transition-colors duration-150 hover:bg-accent/10"
        @click="handleSelect(emoji)"
      >
        {{ emoji }}
      </button>
    </div>
  </div>
</template>
