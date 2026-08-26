<script setup lang="ts">
import { onMounted, ref } from "vue"
import { storeToRefs } from "pinia"
import { useInfiniteScroll } from "@vueuse/core"
import { useMessageStore } from "@/stores/messages"
import { useAuthStore } from "@/stores/auth"
import { notify } from "@/lib/notify"
import { fullName, formatTime } from "@/lib/format"
import Input from "@/components/input.vue"
import Button from "@/components/button.vue"

const PAGE_SIZE = 30

const props = defineProps<{
  chatId: number
}>()

const messageStore = useMessageStore()
const { messages, totalCount } = storeToRefs(messageStore)

const authStore = useAuthStore()
const { user: currentUser } = storeToRefs(authStore)

const scrollContainer = ref<HTMLElement | null>(null)
const text = ref("")
const sending = ref(false)

const infiniteScroll = useInfiniteScroll(
  scrollContainer,
  async () => {
    await messageStore.fetchMessages(PAGE_SIZE, messages.value.length, { append: true })
  },
  {
    direction: "top",
    distance: 100,
    canLoadMore: () => messages.value.length < totalCount.value,
  },
)

onMounted(async () => {
  messageStore.openChat(props.chatId)
  await messageStore.fetchMessages(PAGE_SIZE, 0)
  infiniteScroll.reset()
})

async function handleSubmit() {
  const value = text.value.trim()
  if (value === "") {
    return
  }

  sending.value = true
  try {
    await messageStore.sendMessage(value)
    text.value = ""
  } catch {
    notify.error("Не удалось отправить сообщение")
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <div class="flex h-full flex-1 flex-col">
    <div ref="scrollContainer" class="flex flex-1 flex-col-reverse gap-3 overflow-y-auto px-6 py-4">
      <div
        v-for="message in messages"
        :key="message.id"
        class="flex flex-col gap-1"
        :class="message.user.id === currentUser?.id ? 'items-end' : 'items-start'"
      >
        <div
          class="max-w-md rounded-card px-4 py-2.5 text-[15px]"
          :class="
            message.user.id === currentUser?.id
              ? 'bg-accent text-bg'
              : 'bg-card text-main shadow-card'
          "
        >
          <div
            v-if="message.user.id !== currentUser?.id"
            class="mb-0.5 text-xs font-medium opacity-70"
          >
            {{ fullName(message.user) }}
          </div>
          <div class="whitespace-pre-wrap break-words">{{ message.text }}</div>
        </div>
        <span class="px-1 text-xs text-second">{{ formatTime(message.createdAt) }}</span>
      </div>

      <div v-if="infiniteScroll.isLoading.value" class="py-2 text-center text-sm text-second">
        Загрузка...
      </div>
    </div>

    <form
      class="flex shrink-0 items-center gap-3 border-t border-second/15 px-6 py-4"
      @submit.prevent="handleSubmit"
    >
      <Input v-model="text" placeholder="Написать сообщение..." class="flex-1" />
      <Button
        type="submit"
        icon="send"
        :short-mode="false"
        :disabled="sending || text.trim() === ''"
      >
        Отправить
      </Button>
    </form>
  </div>
</template>
