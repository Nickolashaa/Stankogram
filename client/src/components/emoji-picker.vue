<script setup lang="ts">
import { computed, ref, watch } from "vue"
import { EMOJI_GROUPS } from "@/lib/emoji-data"
import { EMOJI_KEYWORDS } from "@/lib/emoji-keywords"
import Input from "@/components/input.vue"

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
const query = ref("")

function matchesKeywords(keywords: string, emoji: string, token: string) {
  return emoji === token || keywords.startsWith(token) || keywords.includes(` ${token}`)
}

const searchResults = computed(() => {
  const tokens = query.value.trim().toLowerCase().split(/\s+/).filter(Boolean)
  if (tokens.length === 0) {
    return null
  }

  const seen = new Set<string>()
  const matched: string[] = []

  for (const group of EMOJI_GROUPS) {
    for (const emoji of group.emojis) {
      if (seen.has(emoji)) {
        continue
      }
      seen.add(emoji)

      const keywords = EMOJI_KEYWORDS[emoji] ?? ""
      if (tokens.every((token) => matchesKeywords(keywords, emoji, token))) {
        matched.push(emoji)
      }
    }
  }

  return matched
})

const tabs = computed(() =>
  recent.value.length > 0
    ? [{ id: "recent", label: "Недавние", icon: "🕘" }, ...EMOJI_GROUPS]
    : EMOJI_GROUPS,
)

const visibleEmojis = computed(() => {
  if (searchResults.value !== null) {
    return searchResults.value
  }
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
    query.value = ""
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
    class="glass-strong hairline shadow-float absolute right-0 bottom-full z-50 mb-3 flex w-full max-w-sm origin-bottom-right animate-pop flex-col overflow-hidden rounded-card"
  >
    <div class="shrink-0 px-2 pt-2">
      <Input v-model="query" placeholder="Поиск эмодзи..." />
    </div>

    <div
      v-if="searchResults === null"
      class="hairline-b flex shrink-0 gap-0.5 overflow-x-auto px-2 py-2"
    >
      <button
        v-for="tab in tabs"
        :key="tab.id"
        type="button"
        class="press flex h-8 w-8 shrink-0 cursor-pointer items-center justify-center rounded-input text-base"
        :class="
          activeGroupId === tab.id
            ? 'bg-accent/15 ring-1 ring-accent/25 ring-inset'
            : 'hover:bg-main/6'
        "
        :title="tab.label"
        :aria-label="tab.label"
        @click="activeGroupId = tab.id"
      >
        {{ tab.icon }}
      </button>
    </div>

    <div v-if="visibleEmojis.length === 0" class="px-3 py-6 text-center text-sm text-second">
      Ничего не найдено
    </div>

    <div v-else class="grid max-h-56 grid-cols-8 gap-0.5 overflow-y-auto p-2">
      <button
        v-for="(emoji, index) in visibleEmojis"
        :key="`${emoji}-${index}`"
        type="button"
        class="press flex h-9 cursor-pointer items-center justify-center rounded-input text-xl leading-none hover:bg-accent/12"
        @click="handleSelect(emoji)"
      >
        {{ emoji }}
      </button>
    </div>
  </div>
</template>
