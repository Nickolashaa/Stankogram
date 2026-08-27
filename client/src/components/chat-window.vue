<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import { useInfiniteScroll } from "@vueuse/core"
import { useMessageStore } from "@/stores/messages"
import { useAuthStore } from "@/stores/auth"
import { useChatStore, type ChatParticipantItem } from "@/stores/chats"
import { notify } from "@/lib/notify"
import { shortName, formatTime } from "@/lib/format"
import { participantBadges, userBadges } from "@/lib/badges"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import Input from "@/components/input.vue"
import Button from "@/components/button.vue"
import Badge from "@/components/badge.vue"
import NavIcon from "@/components/nav-icon.vue"

const PAGE_SIZE = 30

const props = defineProps<{
  chatId: number
}>()

const messageStore = useMessageStore()
const { messages, totalCount } = storeToRefs(messageStore)

const authStore = useAuthStore()
const { user: currentUser } = storeToRefs(authStore)

const chatStore = useChatStore()
const { chats } = storeToRefs(chatStore)

const participantsByUserId = computed(() => {
  const chat = chats.value.find((item) => item.id === props.chatId)
  const map = new Map<number, ChatParticipantItem>()
  chat?.participants.forEach((participant) => map.set(participant.user.id, participant))
  return map
})

function badgesForSender(user: UserFieldsFragment) {
  const participant = participantsByUserId.value.get(user.id)
  return participant ? participantBadges(user, participant) : userBadges(user)
}

const isMuted = computed(() => {
  const userId = currentUser.value?.id
  if (userId === undefined) {
    return false
  }
  return participantsByUserId.value.get(userId)?.isMuted === true
})

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

watch(
  () => messages.value[0]?.id,
  (newestMessageId) => {
    if (newestMessageId !== undefined) {
      chatStore.markChatRead(props.chatId)
    }
  },
)

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
            class="mb-1 flex flex-wrap items-center gap-1.5 text-xs font-medium opacity-70"
          >
            <span>{{ shortName(message.user) }}</span>
            <Badge
              v-for="badge in badgesForSender(message.user)"
              :key="badge.label"
              :variant="badge.variant"
              :label="badge.label"
            />
          </div>
          <div class="whitespace-pre-wrap break-words">{{ message.text }}</div>
        </div>
        <span class="px-1 text-xs text-second">{{ formatTime(message.createdAt) }}</span>
      </div>

      <div v-if="infiniteScroll.isLoading.value" class="py-2 text-center text-sm text-second">
        Загрузка...
      </div>
    </div>

    <div
      v-if="isMuted"
      class="flex shrink-0 items-center justify-center gap-2 border-t border-second/15 px-6 py-4 text-sm text-second"
    >
      <NavIcon name="mute" :size="16" />
      Вы не можете отправлять сообщения в этом чате
    </div>
    <form
      v-else
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
