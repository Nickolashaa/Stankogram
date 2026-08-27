<script setup lang="ts">
import { onMounted, ref } from "vue"
import { storeToRefs } from "pinia"
import { useRouter } from "vue-router"
import { useInfiniteScroll } from "@vueuse/core"
import { useChatStore } from "@/stores/chats"
import { shortName, formatTime } from "@/lib/format"
import Button from "@/components/button.vue"
import CreateGroupChatDialog from "@/components/create-group-chat-dialog.vue"

const PAGE_SIZE = 30

defineProps<{
  activeChatId: number | null
}>()

const emit = defineEmits<{
  select: [chatId: number]
}>()

const router = useRouter()
const chatStore = useChatStore()
const { chats, totalCount } = storeToRefs(chatStore)

const createGroupOpen = ref(false)

function handleGroupCreated(chatId: number) {
  createGroupOpen.value = false
  router.push(`/chats/${chatId}`)
}

const scrollContainer = ref<HTMLElement | null>(null)

onMounted(() => {
  chatStore.fetchChats(undefined, PAGE_SIZE, 0)
})

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

function lastMessagePreview(chat: (typeof chats.value)[number]) {
  const message = chat.lastMessage
  if (!message) {
    return "Сообщений пока нет"
  }
  return `${shortName(message.user)}: ${message.text}`
}
</script>

<template>
  <div class="flex h-full w-80 shrink-0 flex-col border-r border-second/15 bg-card">
    <div
      class="flex shrink-0 items-center justify-between gap-2 border-b border-second/15 px-5 py-5"
    >
      <h2 class="m-0 text-lg font-semibold text-main">Чаты</h2>
      <Button
        icon="plus"
        title="Новая группа"
        aria-label="Новая группа"
        @click="createGroupOpen = true"
      />
    </div>

    <div ref="scrollContainer" class="flex-1 overflow-y-auto">
      <button
        v-for="chat in chats"
        :key="chat.id"
        type="button"
        class="flex w-full cursor-pointer flex-col gap-1 border-b border-second/10 px-5 py-3 text-left transition-colors duration-150 hover:bg-accent/5"
        :class="chat.id === activeChatId ? 'bg-accent/10' : ''"
        @click="emit('select', chat.id)"
      >
        <div class="flex items-center justify-between gap-2">
          <span class="truncate text-[15px] font-medium text-main">{{ chat.title }}</span>
          <span v-if="chat.lastMessage" class="shrink-0 text-xs text-second">
            {{ formatTime(chat.lastMessage.createdAt) }}
          </span>
        </div>
        <span class="truncate text-sm text-second">{{ lastMessagePreview(chat) }}</span>
      </button>

      <div v-if="chats.length === 0" class="px-5 py-8 text-center text-sm text-second">
        Чатов пока нет
      </div>

      <div v-if="infiniteScroll.isLoading.value" class="py-4 text-center text-sm text-second">
        Загрузка...
      </div>
    </div>

    <CreateGroupChatDialog
      :open="createGroupOpen"
      @close="createGroupOpen = false"
      @created="handleGroupCreated"
    />
  </div>
</template>
