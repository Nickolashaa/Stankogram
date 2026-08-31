<script setup lang="ts">
import { computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import { storeToRefs } from "pinia"
import { useChatStore } from "@/stores/chats"
import AdminChatsListPanel from "@/components/admin-chats-list-panel.vue"
import ChatMetaPanel from "@/components/chat-meta-panel.vue"
import NavIcon from "@/components/nav-icon.vue"

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
  <div class="flex h-full animate-appear flex-col gap-4 lg:flex-row lg:gap-6">
    <AdminChatsListPanel
      :active-chat-id="activeChatId"
      :mobile-hidden="activeChatId !== null"
      @select="selectChat"
    />

    <template v-if="activeChat">
      <div class="flex min-h-0 flex-1 flex-col gap-3 lg:contents">
        <button
          type="button"
          class="flex shrink-0 cursor-pointer items-center gap-2 text-sm font-medium text-second transition-colors duration-150 hover:text-main lg:hidden"
          @click="router.push('/admin/chats')"
        >
          <NavIcon name="arrow-right" :size="16" class="rotate-180" />
          Назад к списку
        </button>
        <ChatMetaPanel
          :key="activeChat.id"
          :chat="activeChat"
          manage
          variant="page"
          @deleted="router.push('/admin/chats')"
        />
      </div>
    </template>
    <div
      v-else
      class="hidden flex-1 items-center justify-center rounded-card bg-card text-second shadow-card lg:flex"
    >
      Выберите групповой чат, чтобы посмотреть и отредактировать информацию о нём
    </div>
  </div>
</template>
