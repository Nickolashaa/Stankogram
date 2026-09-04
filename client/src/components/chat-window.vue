<script setup lang="ts">
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import { useDebounceFn, useInfiniteScroll } from "@vueuse/core"
import { useMessageStore } from "@/stores/messages"
import { useAuthStore } from "@/stores/auth"
import { useChatStore, type ChatParticipantItem, type ChatSummary } from "@/stores/chats"
import { useDraftStore } from "@/stores/drafts"
import { EChatType } from "@/graphql/base-types"
import { notify } from "@/lib/notify"
import { shortName, formatTime, chatInitials } from "@/lib/format"
import { linkify } from "@/lib/linkify"
import { participantBadges, userBadges } from "@/lib/badges"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import Button from "@/components/button.vue"
import Badge from "@/components/badge.vue"
import NavIcon from "@/components/nav-icon.vue"
import Avatar from "@/components/avatar.vue"

const PAGE_SIZE = 30

const props = defineProps<{
  chatId: number
  chat?: ChatSummary | null
}>()

const emit = defineEmits<{
  back: []
  "open-info": []
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

const draftStore = useDraftStore()

const scrollContainer = ref<HTMLElement | null>(null)
const text = ref(draftStore.getDraft(props.chatId))
const sending = ref(false)

const saveDraft = useDebounceFn((value: string) => {
  draftStore.setDraft(props.chatId, value)
}, 300)

watch(text, (value) => {
  saveDraft(value)
})

onUnmounted(() => {
  draftStore.setDraft(props.chatId, text.value)
})

const composerEl = ref<HTMLTextAreaElement | null>(null)
const sendsOnEnter = window.matchMedia("(pointer: fine)").matches

function resizeComposer() {
  const el = composerEl.value
  if (!el) {
    return
  }
  el.style.height = "auto"
  el.style.height = `${el.scrollHeight}px`
}

function handleComposerInput(event: Event) {
  text.value = (event.target as HTMLTextAreaElement).value
  resizeComposer()
}

function handleComposerKeydown(event: KeyboardEvent) {
  if (!sendsOnEnter || event.key !== "Enter" || event.shiftKey || event.isComposing) {
    return
  }

  event.preventDefault()
  handleSubmit()
}

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
  resizeComposer()
  if (sendsOnEnter) {
    composerEl.value?.focus()
  }

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
    draftStore.setDraft(props.chatId, "")
    await nextTick()
    resizeComposer()
  } catch {
    notify.error("Не удалось отправить сообщение")
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <div class="flex h-full w-full flex-1 flex-col">
    <div class="flex shrink-0 items-center gap-3 border-b border-second/15 px-4 py-3 lg:px-6">
      <button
        type="button"
        class="flex h-9 w-9 shrink-0 cursor-pointer items-center justify-center rounded-full text-second transition-colors duration-150 hover:bg-accent/5 hover:text-main lg:hidden"
        aria-label="Назад к чатам"
        @click="emit('back')"
      >
        <NavIcon name="arrow-right" :size="18" class="rotate-180" />
      </button>

      <button
        type="button"
        class="flex min-w-0 flex-1 cursor-pointer items-center gap-3 text-left"
        @click="emit('open-info')"
      >
        <Avatar :label="chatInitials(chat?.title ?? '')" />
        <span class="flex min-w-0 flex-col">
          <span class="truncate text-[15px] font-semibold text-main">{{ chat?.title }}</span>
          <span class="truncate text-xs text-second">
            {{
              chat?.type === EChatType.Public
                ? `${chat.participants.length} участников`
                : "Личный чат"
            }}
          </span>
        </span>
      </button>
    </div>

    <div
      ref="scrollContainer"
      class="flex flex-1 flex-col-reverse gap-3 overflow-y-auto px-4 py-3 lg:px-6 lg:py-4"
    >
      <div
        v-for="message in messages"
        :key="message.id"
        class="flex flex-col gap-1"
        :class="message.user.id === currentUser?.id ? 'items-end' : 'items-start'"
      >
        <div
          class="max-w-[min(28rem,85%)] rounded-card px-4 py-2.5 text-[15px]"
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
          <div class="whitespace-pre-wrap break-words">
            <template v-for="(segment, index) in linkify(message.text)" :key="index">
              <a
                v-if="segment.type === 'link'"
                :href="segment.href"
                target="_blank"
                rel="noopener noreferrer nofollow"
                class="underline underline-offset-2 transition-opacity hover:opacity-70"
                >{{ segment.value }}</a
              >
              <template v-else>{{ segment.value }}</template>
            </template>
          </div>
        </div>
        <span class="px-1 text-xs text-second">{{ formatTime(message.createdAt) }}</span>
      </div>

      <div v-if="infiniteScroll.isLoading.value" class="py-2 text-center text-sm text-second">
        Загрузка...
      </div>
    </div>

    <div
      v-if="isMuted"
      class="flex shrink-0 items-center justify-center gap-2 border-t border-second/15 px-4 pt-3 pb-[calc(1.25rem+env(safe-area-inset-bottom))] text-sm text-second lg:px-6 lg:py-4"
    >
      <NavIcon name="mute" :size="16" />
      Вы не можете отправлять сообщения в этом чате
    </div>
    <form
      v-else
      class="flex shrink-0 items-end gap-3 border-t border-second/15 px-4 pt-3 pb-[calc(1.25rem+env(safe-area-inset-bottom))] lg:px-6 lg:py-4"
      @submit.prevent="handleSubmit"
    >
      <textarea
        ref="composerEl"
        :value="text"
        rows="1"
        placeholder="Сообщение..."
        name="message"
        autocomplete="off"
        autocapitalize="sentences"
        autocorrect="on"
        spellcheck="true"
        :enterkeyhint="sendsOnEnter ? 'send' : 'enter'"
        class="box-border max-h-40 min-h-12 min-w-0 flex-1 resize-none overflow-y-auto rounded-input border-[1.5px] border-second/30 bg-bg px-4 py-3 font-sans text-[15px] leading-6 text-main outline-none transition-colors duration-150 placeholder:overflow-hidden placeholder:text-ellipsis placeholder:whitespace-nowrap placeholder:text-second focus:border-accent"
        @input="handleComposerInput"
        @keydown="handleComposerKeydown"
      />
      <Button
        type="submit"
        icon="send"
        title="Отправить"
        aria-label="Отправить"
        :disabled="sending || text.trim() === ''"
      />
    </form>
  </div>
</template>
