<script setup lang="ts">
import { computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import { storeToRefs } from "pinia"
import { useChatStore } from "@/stores/chats"
import AdminPage from "@/components/admin-page.vue"
import AdminChatsListPanel from "@/components/admin-chats-list-panel.vue"
import ChatMetaPanel from "@/components/chat-meta-panel.vue"
import NavIcon from "@/components/nav-icon.vue"

const route = useRoute()
const router = useRouter()

const chatStore = useChatStore()
const { adminChats, adminTotalCount } = storeToRefs(chatStore)

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
  <AdminPage title="Групповые чаты" :total="adminTotalCount" fill>
    <div class="flex min-h-0 flex-1 flex-col gap-4 xl:flex-row xl:gap-6">
      <AdminChatsListPanel
        :active-chat-id="activeChatId"
        :mobile-hidden="activeChatId !== null"
        @select="selectChat"
      />

      <template v-if="activeChat">
        <div class="flex min-h-0 flex-1 flex-col gap-3 xl:contents">
          <button
            type="button"
            class="press glass hairline flex w-fit shrink-0 cursor-pointer items-center gap-2 rounded-full px-3.5 py-2 text-sm font-medium text-second hover:text-main xl:hidden"
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
        class="glass hairline shadow-card hidden flex-1 items-center justify-center rounded-card p-10 text-center text-sm text-second xl:flex"
      >
        <span class="max-w-sm">
          Выберите групповой чат, чтобы посмотреть и отредактировать информацию о нём
        </span>
      </div>
    </div>
  </AdminPage>
</template>
