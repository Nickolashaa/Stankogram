<script setup lang="ts">
import { computed, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { storeToRefs } from "pinia"
import { useChatStore } from "@/stores/chats"
import ChatsListPanel from "@/components/chats-list-panel.vue"
import ChatWindow from "@/components/chat-window.vue"
import ChatMetaPanel from "@/components/chat-meta-panel.vue"
import NavIcon from "@/components/nav-icon.vue"

const route = useRoute()
const router = useRouter()

const chatStore = useChatStore()
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

const mobileInfoOpen = ref(false)

watch(activeChatId, () => {
  mobileInfoOpen.value = false
})
</script>

<template>
  <div class="flex h-dvh">
    <ChatsListPanel
      :active-chat-id="activeChatId"
      :mobile-hidden="activeChatId !== null"
      @select="selectChat"
    />

    <template v-if="activeChatId !== null">
      <ChatWindow
        :key="activeChatId"
        :chat-id="activeChatId"
        :chat="activeChat"
        @back="router.push('/chats')"
        @open-info="mobileInfoOpen = true"
      />
      <div v-if="activeChat" class="hidden h-full lg:block">
        <ChatMetaPanel :chat="activeChat" />
      </div>

      <div
        v-if="mobileInfoOpen && activeChat"
        class="fixed inset-0 z-50 flex animate-appear justify-end bg-black/40 p-3 lg:hidden"
        @click.self="mobileInfoOpen = false"
      >
        <div class="relative flex h-full w-full max-w-sm flex-col">
          <button
            type="button"
            class="absolute top-4 right-4 z-10 flex h-9 w-9 cursor-pointer items-center justify-center rounded-full bg-card text-second shadow-card"
            aria-label="Закрыть"
            @click="mobileInfoOpen = false"
          >
            <NavIcon name="cancel" />
          </button>
          <ChatMetaPanel :chat="activeChat" variant="page" class="h-full" />
        </div>
      </div>
    </template>
    <div v-else class="hidden flex-1 items-center justify-center text-second lg:flex">
      Выберите чат, чтобы начать переписку
    </div>
  </div>
</template>
