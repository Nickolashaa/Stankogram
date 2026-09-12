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

function handleLeft() {
  mobileInfoOpen.value = false
  router.push("/chats")
}

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
        <ChatMetaPanel :chat="activeChat" @left="handleLeft" />
      </div>

      <div
        v-if="mobileInfoOpen && activeChat"
        class="fixed inset-0 z-50 flex animate-appear justify-end bg-black/45 p-3 backdrop-blur-sm lg:hidden"
        @click.self="mobileInfoOpen = false"
      >
        <div class="relative flex h-full w-full max-w-sm animate-pop flex-col">
          <button
            type="button"
            class="press glass-strong hairline shadow-pop absolute top-4 right-4 z-10 flex h-9 w-9 cursor-pointer items-center justify-center rounded-full text-second hover:text-main"
            aria-label="Закрыть"
            @click="mobileInfoOpen = false"
          >
            <NavIcon name="cancel" />
          </button>
          <ChatMetaPanel :chat="activeChat" variant="page" class="h-full" @left="handleLeft" />
        </div>
      </div>
    </template>
    <div class="hidden flex-1 items-center justify-center p-10 lg:flex" v-else>
      <div
        class="glass hairline shadow-card flex animate-rise flex-col items-center gap-3 rounded-card px-10 py-12 text-center"
      >
        <span class="chip-accent glow-accent-soft flex h-14 w-14 items-center justify-center">
          <NavIcon name="chats" :size="26" />
        </span>
        <span class="text-[15px] font-medium text-main">Выберите чат</span>
        <span class="max-w-xs text-sm text-second">
          Откройте диалог из списка слева или создайте новый, чтобы начать переписку
        </span>
      </div>
    </div>
  </div>
</template>
