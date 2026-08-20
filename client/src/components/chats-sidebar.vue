<script setup lang="ts">
import type { components } from "@/api/schema"

type ChatProfileResponse = components["schemas"]["ChatProfileResponse"]

defineProps<{
  chats: ChatProfileResponse[]
  selectedChatId: number | null
}>()

defineEmits<{
  select: [chatId: number]
}>()
</script>

<template>
  <div class="flex w-80 shrink-0 flex-col gap-1 overflow-y-auto border-r border-second/15 p-3">
    <button
      v-for="item in chats"
      :key="item.chat.id"
      type="button"
      class="cursor-pointer rounded-input px-4 py-3 text-left text-[15px] font-medium text-second transition-colors duration-150 hover:bg-accent/10 hover:text-main"
      :class="item.chat.id === selectedChatId ? 'bg-accent/10 text-accent' : ''"
      @click="$emit('select', item.chat.id)"
    >
      {{ item.title }}
    </button>

    <div v-if="chats.length === 0" class="px-4 py-8 text-center text-sm text-second">
      Чатов пока нет
    </div>
  </div>
</template>
