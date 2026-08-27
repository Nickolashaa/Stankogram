<script setup lang="ts">
import { computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import { storeToRefs } from "pinia"
import { useChatStore } from "@/stores/chats"
import AdminChatsListPanel from "@/components/admin-chats-list-panel.vue"
import ChatMetaPanel from "@/components/chat-meta-panel.vue"

const route = useRoute()
const router = useRouter()

const chatStore = useChatStore()
const { adminChats } = storeToRefs(chatStore)

const activeChatId = computed(() => {
  const raw = route.params.chatId
  const id = Number(Array.isArray(raw) ? raw[0] : raw)
  return Number.isInteger(id) && id > 0 ? id : null
})

const activeChat = computed(
  () => adminChats.value.find((chat) => chat.id === activeChatId.value) ?? null,
)

function selectChat(chatId: number) {
  router.push(`/admin/chats/${chatId}`)
}
</script>

<template>
  <div class="flex h-full animate-appear gap-6">
    <AdminChatsListPanel :active-chat-id="activeChatId" @select="selectChat" />

    <ChatMetaPanel
      v-if="activeChat"
      :key="activeChat.id"
      :chat="activeChat"
      manage
      variant="page"
    />
    <div
      v-else
      class="flex flex-1 items-center justify-center rounded-card bg-card text-second shadow-card"
    >
      Выберите групповой чат, чтобы посмотреть и отредактировать информацию о нём
    </div>
  </div>
</template>
