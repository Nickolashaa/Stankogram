<script setup lang="ts">
import { computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import { storeToRefs } from "pinia"
import { useChatStore } from "@/stores/chats"
import { useMessageStore } from "@/stores/messages"
import { useEventsSubscription } from "@/graphql/subscriptions/events.generated"
import ChatsListPanel from "@/components/chats-list-panel.vue"
import ChatWindow from "@/components/chat-window.vue"
import ChatMetaPanel from "@/components/chat-meta-panel.vue"

const route = useRoute()
const router = useRouter()

const chatStore = useChatStore()
const messageStore = useMessageStore()
const { chats } = storeToRefs(chatStore)

const activeChatId = computed(() => {
  const raw = route.params.chatId
  const id = Number(Array.isArray(raw) ? raw[0] : raw)
  return Number.isInteger(id) && id > 0 ? id : null
})

const activeChat = computed(
  () => chats.value.find((chat) => chat.id === activeChatId.value) ?? null,
)

function selectChat(chatId: number) {
  router.push(`/chats/${chatId}`)
}

const { onResult } = useEventsSubscription()

onResult(({ data }) => {
  if (!data) {
    return
  }

  chatStore.handleIncomingMessage(data.events)
  messageStore.handleIncomingMessage(data.events)
})
</script>

<template>
  <div class="flex h-screen">
    <ChatsListPanel :active-chat-id="activeChatId" @select="selectChat" />

    <template v-if="activeChatId !== null">
      <ChatWindow :key="activeChatId" :chat-id="activeChatId" />
      <ChatMetaPanel v-if="activeChat" :chat="activeChat" />
    </template>
    <div v-else class="flex flex-1 items-center justify-center text-second">
      Выберите чат, чтобы начать переписку
    </div>
  </div>
</template>
