<script setup lang="ts">
import { computed, onMounted } from "vue"
import { useRoute } from "vue-router"
import { useChatStore } from "@/stores/chats"
import { useMessageStore } from "@/stores/messages"
import { useEventsSubscription } from "@/graphql/subscriptions/events.generated"
import AppNav from "@/components/app-nav.vue"

const CHATS_PAGE_SIZE = 30

const route = useRoute()
const isChatsRoute = computed(() => route.path.startsWith("/chats"))

const chatStore = useChatStore()
const messageStore = useMessageStore()

onMounted(() => {
  if (chatStore.chats.length === 0) {
    chatStore.fetchChats(undefined, CHATS_PAGE_SIZE, 0)
  }
})

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
  <div class="flex h-dvh">
    <AppNav />
    <div class="flex-1 overflow-y-auto" :class="isChatsRoute ? '' : 'pb-16 lg:pb-0'">
      <RouterView />
    </div>
  </div>
</template>
