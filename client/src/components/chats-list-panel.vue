<script setup lang="ts">
import { onMounted, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import { useRouter } from "vue-router"
import { useInfiniteScroll } from "@vueuse/core"
import { useChatStore, hasUnreadMessages } from "@/stores/chats"
import { useAuthStore } from "@/stores/auth"
import { useDraftStore } from "@/stores/drafts"
import { shortName, formatTime, chatInitials } from "@/lib/format"
import Button from "@/components/button.vue"
import Avatar from "@/components/avatar.vue"
import NavIcon from "@/components/nav-icon.vue"
import CreateGroupChatDialog from "@/components/create-group-chat-dialog.vue"
import CreatePrivateChatDialog from "@/components/create-private-chat-dialog.vue"

const PAGE_SIZE = 30

const props = defineProps<{
  activeChatId: number | null
  mobileHidden?: boolean
}>()

const emit = defineEmits<{
  select: [chatId: number]
}>()

const router = useRouter()
const chatStore = useChatStore()
const authStore = useAuthStore()
const draftStore = useDraftStore()
const { chats, totalCount } = storeToRefs(chatStore)
const { user: currentUser } = storeToRefs(authStore)

function isUnread(chat: (typeof chats.value)[number]) {
  return currentUser.value !== undefined && hasUnreadMessages(chat, currentUser.value.id)
}

const createGroupOpen = ref(false)
const createPrivateOpen = ref(false)
const createMenuOpen = ref(false)

function openPrivateChatDialog() {
  createMenuOpen.value = false
  createPrivateOpen.value = true
}

function openGroupChatDialog() {
  createMenuOpen.value = false
  createGroupOpen.value = true
}

function handlePrivateCreated(chatId: number) {
  createPrivateOpen.value = false
  router.push(`/chats/${chatId}`)
}

function handleGroupCreated(chatId: number) {
  createGroupOpen.value = false
  router.push(`/chats/${chatId}`)
}

const scrollContainer = ref<HTMLElement | null>(null)

const infiniteScroll = useInfiniteScroll(
  scrollContainer,
  async () => {
    await chatStore.fetchChats(undefined, PAGE_SIZE, chats.value.length, { append: true })
  },
  {
    distance: 100,
    canLoadMore: () => chats.value.length < totalCount.value,
  },
)

async function refreshChats() {
  await chatStore.fetchChats(undefined, PAGE_SIZE, 0)
  infiniteScroll.reset()
}

onMounted(refreshChats)

watch(
  () => props.activeChatId,
  (chatId) => {
    if (chatId === null) {
      refreshChats()
    }
  },
)

function lastMessagePreview(chat: (typeof chats.value)[number]) {
  const message = chat.lastMessage
  if (!message) {
    return "Сообщений пока нет"
  }
  return `${shortName(message.user)}: ${message.text}`
}
</script>

<template>
  <div
    class="glass h-full w-full shrink-0 flex-col lg:flex lg:w-84 lg:hairline-r"
    :class="mobileHidden ? 'hidden' : 'flex'"
  >
    <div class="hairline-b flex shrink-0 items-center justify-between gap-2 px-5 py-4">
      <h2 class="m-0 text-xl font-semibold tracking-tight text-main">Чаты</h2>

      <div class="relative">
        <Button
          icon="plus"
          title="Новый чат"
          aria-label="Новый чат"
          @click="createMenuOpen = !createMenuOpen"
        />

        <div v-if="createMenuOpen" class="fixed inset-0 z-40" @click="createMenuOpen = false" />

        <div
          v-if="createMenuOpen"
          class="glass-strong hairline shadow-float absolute top-full right-0 z-50 mt-2 flex w-68 origin-top-right animate-pop flex-col gap-1 rounded-card p-2"
        >
          <button
            type="button"
            class="press flex cursor-pointer items-center gap-3 rounded-input px-3 py-2.5 text-left hover:bg-main/5"
            @click="openPrivateChatDialog"
          >
            <span class="chip-accent flex h-9 w-9 shrink-0 items-center justify-center">
              <NavIcon name="users" :size="18" />
            </span>
            <span class="flex min-w-0 flex-col gap-0.5">
              <span class="text-[15px] font-medium text-main">Личный чат</span>
              <span class="truncate text-xs text-second">Найти коллегу и написать ему</span>
            </span>
          </button>

          <button
            type="button"
            class="press flex cursor-pointer items-center gap-3 rounded-input px-3 py-2.5 text-left hover:bg-main/5"
            @click="openGroupChatDialog"
          >
            <span class="chip-accent flex h-9 w-9 shrink-0 items-center justify-center">
              <NavIcon name="chats" :size="18" />
            </span>
            <span class="flex min-w-0 flex-col gap-0.5">
              <span class="text-[15px] font-medium text-main">Групповой чат</span>
              <span class="truncate text-xs text-second">Создать группу с участниками</span>
            </span>
          </button>
        </div>
      </div>
    </div>

    <div
      ref="scrollContainer"
      class="flex flex-1 flex-col gap-1 overflow-y-auto px-2.5 pt-2.5 pb-[calc(var(--design-nav-offset)+env(safe-area-inset-bottom))] lg:pb-3"
    >
      <button
        v-for="chat in chats"
        :key="chat.id"
        type="button"
        class="press flex w-full cursor-pointer items-center gap-3 rounded-card px-3 py-2.5 text-left"
        :class="chat.id === activeChatId ? 'pill-active' : 'pill-idle'"
        @click="emit('select', chat.id)"
      >
        <Avatar :label="chatInitials(chat.title)" />

        <div class="flex min-w-0 flex-1 flex-col gap-0.5">
          <div class="flex items-center justify-between gap-2">
            <span
              class="truncate text-[15px] text-main"
              :class="isUnread(chat) ? 'font-semibold' : 'font-medium'"
            >
              {{ chat.title }}
            </span>
            <span v-if="chat.lastMessage" class="shrink-0 text-xs text-second/80">
              {{ formatTime(chat.lastMessage.createdAt) }}
            </span>
          </div>
          <div class="flex items-center justify-between gap-2">
            <span
              class="truncate text-sm"
              :class="isUnread(chat) ? 'font-medium text-main' : 'text-second'"
            >
              <template v-if="draftStore.getDraft(chat.id)">
                <span class="text-accent">Черновик:</span> {{ draftStore.getDraft(chat.id) }}
              </template>
              <template v-else>{{ lastMessagePreview(chat) }}</template>
            </span>
            <span
              v-if="isUnread(chat)"
              class="glow-accent h-2 w-2 shrink-0 rounded-full bg-accent"
            />
          </div>
        </div>
      </button>

      <div v-if="chats.length === 0" class="px-5 py-8 text-center text-sm text-second">
        Чатов пока нет
      </div>

      <div v-if="infiniteScroll.isLoading.value" class="py-4 text-center text-sm text-second">
        Загрузка...
      </div>
    </div>

    <CreatePrivateChatDialog
      :open="createPrivateOpen"
      @close="createPrivateOpen = false"
      @created="handlePrivateCreated"
    />

    <CreateGroupChatDialog
      :open="createGroupOpen"
      @close="createGroupOpen = false"
      @created="handleGroupCreated"
    />
  </div>
</template>
