<script setup lang="ts">
import type { ChatSummary } from "@/stores/chats"
import { EChatType } from "@/graphql/base-types"
import { fullName } from "@/lib/format"
import { participantBadges } from "@/lib/badges"
import Badge from "@/components/badge.vue"

defineProps<{
  chat: ChatSummary
}>()

const chatTypeLabels: Record<EChatType, string> = {
  [EChatType.Private]: "Личный чат",
  [EChatType.Public]: "Групповой чат",
}
</script>

<template>
  <div class="flex h-full w-80 shrink-0 flex-col overflow-y-auto border-l border-second/15 bg-card">
    <div class="flex flex-col gap-1 border-b border-second/15 px-6 py-6">
      <h2 class="m-0 text-lg font-semibold text-main">{{ chat.title }}</h2>
      <span class="text-sm text-second">{{ chatTypeLabels[chat.type] }}</span>
    </div>

    <div class="flex flex-col gap-3 px-6 py-5">
      <span class="text-xs font-medium uppercase tracking-wide text-second">
        Участники ({{ chat.participants.length }})
      </span>

      <div class="flex flex-col gap-3">
        <div
          v-for="participant in chat.participants"
          :key="participant.id"
          class="flex flex-col gap-1.5"
        >
          <span class="text-[15px] font-medium text-main">{{ fullName(participant.user) }}</span>
          <div class="flex flex-wrap gap-1.5">
            <Badge
              v-for="badge in participantBadges(participant.user, participant)"
              :key="badge.label"
              :variant="badge.variant"
            >
              {{ badge.label }}
            </Badge>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
