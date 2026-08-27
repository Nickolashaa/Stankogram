<script setup lang="ts">
import { onMounted, ref } from "vue"
import { storeToRefs } from "pinia"
import { useInfiniteScroll } from "@vueuse/core"
import { useChatStore } from "@/stores/chats"
import { EChatType } from "@/graphql/base-types"

const PAGE_SIZE = 30

defineProps<{
  activeChatId: number | null
  mobileHidden?: boolean
}>()

const emit = defineEmits<{
  select: [chatId: number]
}>()

const chatStore = useChatStore()
const { adminChats, adminTotalCount } = storeToRefs(chatStore)

const scrollContainer = ref<HTMLElement | null>(null)

onMounted(() => {
  chatStore.fetchAdminChats({ type: EChatType.Public }, PAGE_SIZE, 0)
})

const infiniteScroll = useInfiniteScroll(
  scrollContainer,
  async () => {
    await chatStore.fetchAdminChats(
      { type: EChatType.Public },
      PAGE_SIZE,
      adminChats.value.length,
      { append: true },
    )
  },
  {
    distance: 100,
    canLoadMore: () => adminChats.value.length < adminTotalCount.value,
  },
)
</script>

<template>
  <div
    class="h-full w-full shrink-0 flex-col overflow-hidden rounded-card bg-card shadow-card lg:flex lg:w-80"
    :class="mobileHidden ? 'hidden' : 'flex'"
  >
    <div class="shrink-0 border-b border-second/15 px-5 py-5">
      <h2 class="m-0 text-lg font-semibold text-main">Групповые чаты</h2>
      <span class="text-sm text-second">Всего: {{ adminTotalCount }}</span>
    </div>

    <div ref="scrollContainer" class="flex-1 overflow-y-auto">
      <button
        v-for="chat in adminChats"
        :key="chat.id"
        type="button"
        class="flex w-full cursor-pointer flex-col gap-1 border-b border-second/10 px-5 py-3 text-left transition-colors duration-150 hover:bg-accent/5"
        :class="chat.id === activeChatId ? 'bg-accent/10' : ''"
        @click="emit('select', chat.id)"
      >
        <span class="truncate text-[15px] font-medium text-main">{{ chat.title }}</span>
        <span class="truncate text-xs text-second">
          Участников: {{ chat.participants.length }}
        </span>
      </button>

      <div v-if="adminChats.length === 0" class="px-5 py-8 text-center text-sm text-second">
        Групповых чатов пока нет
      </div>

      <div v-if="infiniteScroll.isLoading.value" class="py-4 text-center text-sm text-second">
        Загрузка...
      </div>
    </div>
  </div>
</template>
