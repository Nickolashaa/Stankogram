<script setup lang="ts">
import { computed, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import { useChatStore } from "@/stores/chats"
import { useMessageStore } from "@/stores/messages"
import { useEventsSubscription } from "@/graphql/subscriptions/events.generated"
import { EChatType } from "@/graphql/base-types"
import { notify } from "@/lib/notify"
import AppNav from "@/components/app-nav.vue"

const CHATS_PAGE_SIZE = 30

const route = useRoute()
const router = useRouter()
const isChatsRoute = computed(() => route.path.startsWith("/chats"))

const authStore = useAuthStore()
const chatStore = useChatStore()
const messageStore = useMessageStore()

onMounted(() => {
  if (chatStore.chats.length === 0) {
    chatStore.fetchChats(undefined, CHATS_PAGE_SIZE, 0)
  }
})

function handleRemoveParticipant(chatId: number, userId: number) {
  const isSelf = userId === authStore.user?.id
  const isPrivate = chatStore.chats.find((chat) => chat.id === chatId)?.type === EChatType.Private

  chatStore.handleRemoveParticipant(chatId, userId)

  if ((!isSelf && !isPrivate) || Number(route.params.chatId) !== chatId) {
    return
  }

  notify.info(isSelf ? "Вас удалили из чата" : "Чат удалён")
  router.push("/chats")
}

const { onResult } = useEventsSubscription()

onResult(({ data }) => {
  if (!data) {
    return
  }

  const event = data.events

  switch (event.__typename) {
    case "CreateMessage":
      chatStore.handleCreateMessage(event.message)
      messageStore.handleCreateMessage(event.message)
      break
    case "UpdateMessage":
      chatStore.handleUpdateMessage(event.message)
      messageStore.handleUpdateMessage(event.message)
      break
    case "DeleteMessage":
      chatStore.handleDeleteMessage(event.message)
      messageStore.handleDeleteMessage(event.message)
      break
    case "AddChatParticipant":
      chatStore.handleAddParticipant(event.chatId, event.participant)
      break
    case "RemoveChatParticipant":
      handleRemoveParticipant(event.chatId, event.participant.user.id)
      break
  }
})
</script>

<template>
  <div class="flex h-dvh">
    <AppNav />
    <div
      class="flex-1 overflow-y-auto"
      :class="
        isChatsRoute
          ? ''
          : 'pb-[calc(var(--design-nav-offset)+env(safe-area-inset-bottom))] lg:pb-0'
      "
    >
      <RouterView />
    </div>
  </div>
</template>
