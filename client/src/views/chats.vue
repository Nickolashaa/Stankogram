<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import { useRoute, useRouter } from "vue-router"
import { useChatStore } from "@/stores/chats"
import { useMessageStore } from "@/stores/messages"
import { useAuthStore } from "@/stores/auth"
import { notify } from "@/lib/notify"
import ChatsSidebar from "@/components/chats-sidebar.vue"
import ChatThread from "@/components/chat-thread.vue"

const MESSAGES_POLL_INTERVAL_MS = 3000

const route = useRoute()
const router = useRouter()
const chatStore = useChatStore()
const messageStore = useMessageStore()
const authStore = useAuthStore()
const { chats } = storeToRefs(chatStore)
const { messages } = storeToRefs(messageStore)
const { user: currentUser } = storeToRefs(authStore)

const selectedChatId = ref<number | null>(null)
const sending = ref(false)
let pollHandle: ReturnType<typeof setInterval> | undefined

const selectedChat = computed(() =>
  chats.value.find((item) => item.chat.id === selectedChatId.value),
)

function selectChat(chatId: number) {
  router.push({ path: "/chats", query: { chat: chatId } })
}

function stopPolling() {
  if (pollHandle !== undefined) {
    clearInterval(pollHandle)
    pollHandle = undefined
  }
}

async function openChat(chatId: number) {
  selectedChatId.value = chatId
  stopPolling()
  await messageStore.fetchMessages(chatId)
  pollHandle = setInterval(() => messageStore.fetchMessages(chatId), MESSAGES_POLL_INTERVAL_MS)
}

watch(
  () => route.query.chat,
  (value) => {
    const chatId = Number(value)
    if (Number.isInteger(chatId) && chatId > 0) {
      openChat(chatId)
    }
  },
  { immediate: true },
)

async function handleSend(text: string) {
  if (selectedChatId.value === null) {
    return
  }

  sending.value = true
  try {
    await messageStore.sendMessage(selectedChatId.value, text)
  } catch {
    notify.error("Не удалось отправить сообщение")
  } finally {
    sending.value = false
  }
}

onMounted(async () => {
  await chatStore.fetchChats()

  const firstChat = chats.value[0]
  if (selectedChatId.value === null && route.query.chat === undefined && firstChat !== undefined) {
    selectChat(firstChat.chat.id)
  }
})
onUnmounted(stopPolling)
</script>

<template>
  <div class="flex h-full min-h-screen animate-appear">
    <ChatsSidebar :chats="chats" :selected-chat-id="selectedChatId" @select="selectChat" />

    <ChatThread
      v-if="selectedChat && currentUser"
      :key="selectedChat.chat.id"
      :title="selectedChat.title"
      :messages="messages"
      :current-user-id="currentUser.id"
      :sending="sending"
      @send="handleSend"
    />
    <div v-else class="flex flex-1 items-center justify-center text-second">
      Выберите чат, чтобы начать переписку
    </div>
  </div>
</template>
