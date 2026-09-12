<script setup lang="ts">
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import { useDebounceFn, useInfiniteScroll } from "@vueuse/core"
import { useMessageStore, type MessageItem } from "@/stores/messages"
import { useAuthStore } from "@/stores/auth"
import { useChatStore, type ChatParticipantItem, type ChatSummary } from "@/stores/chats"
import { useDraftStore } from "@/stores/drafts"
import { EChatType } from "@/graphql/base-types"
import { notify } from "@/lib/notify"
import { shortName, formatTime, chatInitials, isSameDay, formatDaySeparator } from "@/lib/format"
import { linkify } from "@/lib/linkify"
import { isLargeEmojiMessage } from "@/lib/emoji"
import { participantBadges, userBadges } from "@/lib/badges"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import Button from "@/components/button.vue"
import Badge from "@/components/badge.vue"
import NavIcon from "@/components/nav-icon.vue"
import Avatar from "@/components/avatar.vue"
import EmojiPicker from "@/components/emoji-picker.vue"

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

const isCurrentUserChatAdmin = computed(() => {
  if (currentUser.value?.isAdmin === true) {
    return true
  }
  const userId = currentUser.value?.id
  if (userId === undefined) {
    return false
  }
  return participantsByUserId.value.get(userId)?.isAdmin === true
})

function canEditMessage(message: MessageItem) {
  return message.user.id === currentUser.value?.id
}

function canDeleteMessage(message: MessageItem) {
  return message.user.id === currentUser.value?.id || isCurrentUserChatAdmin.value
}

type MessageContextMenu = {
  x: number
  y: number
  message: MessageItem
}

const MESSAGE_MENU_WIDTH = 180
const MESSAGE_MENU_HEIGHT = 90

const contextMenu = ref<MessageContextMenu | null>(null)

function closeContextMenu() {
  contextMenu.value = null
}

function handleMessageContextMenu(event: MouseEvent, message: MessageItem) {
  if (!canEditMessage(message) && !canDeleteMessage(message)) {
    return
  }
  event.preventDefault()
  contextMenu.value = {
    x: Math.min(event.clientX, window.innerWidth - MESSAGE_MENU_WIDTH - 8),
    y: Math.min(event.clientY, window.innerHeight - MESSAGE_MENU_HEIGHT - 8),
    message,
  }
}

function handleMessageMenuEscape(event: KeyboardEvent) {
  if (event.key === "Escape") {
    closeContextMenu()
  }
}

onMounted(() => window.addEventListener("keydown", handleMessageMenuEscape))
onUnmounted(() => window.removeEventListener("keydown", handleMessageMenuEscape))

const editingMessageId = ref<number | null>(null)
const editDraft = ref("")
const savingEdit = ref(false)

function startEdit(message: MessageItem) {
  editingMessageId.value = message.id
  editDraft.value = message.text
}

function cancelEdit() {
  editingMessageId.value = null
  editDraft.value = ""
}

async function saveEdit() {
  const messageId = editingMessageId.value
  if (messageId === null) {
    return
  }
  const value = editDraft.value.trim()
  if (value === "") {
    return
  }

  savingEdit.value = true
  try {
    await messageStore.updateMessage(messageId, value)
    cancelEdit()
  } catch {
    notify.error("Не удалось изменить сообщение")
  } finally {
    savingEdit.value = false
  }
}

function handleMenuEdit() {
  const message = contextMenu.value?.message
  closeContextMenu()
  if (message !== undefined) {
    startEdit(message)
  }
}

async function handleMenuDelete() {
  const message = contextMenu.value?.message
  closeContextMenu()
  if (message === undefined || !window.confirm("Удалить сообщение?")) {
    return
  }

  try {
    await messageStore.deleteMessage(message.id)
  } catch {
    notify.error("Не удалось удалить сообщение")
  }
}

watch(
  () => props.chatId,
  () => {
    closeContextMenu()
    cancelEdit()
  },
)

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

const emojiPickerOpen = ref(false)

function insertEmoji(emoji: string) {
  const el = composerEl.value
  const start = el?.selectionStart ?? text.value.length
  const end = el?.selectionEnd ?? text.value.length

  text.value = `${text.value.slice(0, start)}${emoji}${text.value.slice(end)}`

  nextTick(() => {
    resizeComposer()
    if (el === null || el === undefined) {
      return
    }
    const caret = start + emoji.length
    el.focus()
    el.setSelectionRange(caret, caret)
  })
}

function handleComposerKeydown(event: KeyboardEvent) {
  if (!sendsOnEnter || event.key !== "Enter" || event.shiftKey || event.isComposing) {
    return
  }

  event.preventDefault()
  handleSubmit()
}

function isFirstMessageOfDay(index: number) {
  const message = messages.value[index]
  if (message === undefined) {
    return false
  }

  const older = messages.value[index + 1]
  if (older === undefined) {
    return true
  }

  return !isSameDay(message.createdAt, older.createdAt)
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
    <div class="glass hairline-b z-10 flex shrink-0 items-center gap-3 px-3 py-3 lg:px-5">
      <button
        type="button"
        class="press flex h-10 w-10 shrink-0 cursor-pointer items-center justify-center rounded-full text-second hover:bg-main/6 hover:text-main lg:hidden"
        aria-label="Назад к чатам"
        @click="emit('back')"
      >
        <NavIcon name="arrow-right" :size="18" class="rotate-180" />
      </button>

      <button
        type="button"
        class="press flex min-w-0 flex-1 cursor-pointer items-center gap-3 rounded-card px-2 py-1.5 text-left hover:bg-main/5"
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
      <template v-for="(message, index) in messages" :key="message.id">
        <div
          class="flex flex-col gap-1"
          :class="[
            message.user.id === currentUser?.id ? 'items-end' : 'items-start',
            canEditMessage(message) || canDeleteMessage(message) ? 'cursor-context-menu' : '',
          ]"
          @contextmenu="handleMessageContextMenu($event, message)"
        >
          <div
            v-if="editingMessageId === message.id"
            class="glass-strong hairline shadow-pop flex w-[min(28rem,85%)] flex-col gap-2 rounded-card px-4 py-2.5 text-[15px] text-main"
          >
            <textarea
              v-model="editDraft"
              rows="1"
              autofocus
              class="max-h-40 min-h-9 w-full resize-none overflow-y-auto bg-transparent font-sans text-[15px] leading-6 text-main outline-none"
              @keydown.enter.exact.prevent="saveEdit"
              @keydown.esc="cancelEdit"
            />
            <div class="flex items-center justify-end gap-2">
              <button
                type="button"
                class="press cursor-pointer rounded-full px-2.5 py-1 text-xs font-medium text-second hover:bg-main/6 hover:text-main"
                @click="cancelEdit"
              >
                Отмена
              </button>
              <button
                type="button"
                class="press cursor-pointer rounded-full bg-accent/12 px-2.5 py-1 text-xs font-medium text-accent hover:bg-accent/22 disabled:cursor-not-allowed disabled:opacity-60"
                :disabled="savingEdit || editDraft.trim() === ''"
                @click="saveEdit"
              >
                Сохранить
              </button>
            </div>
          </div>
          <div
            v-else
            class="max-w-[min(28rem,85%)] rounded-card transition-transform duration-200"
            :class="[
              isLargeEmojiMessage(message.text)
                ? 'px-1 py-0.5 text-5xl leading-tight'
                : 'px-4 py-2.5 text-[15px]',
              isLargeEmojiMessage(message.text)
                ? 'text-main'
                : message.user.id === currentUser?.id
                  ? 'accent-surface glow-accent bubble-own text-bg'
                  : 'glass hairline shadow-card bubble-other text-main',
            ]"
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
              <template
                v-for="(segment, segmentIndex) in linkify(message.text)"
                :key="segmentIndex"
              >
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
          <span class="flex items-center gap-1 px-1.5 text-xs text-second/80">
            <template v-if="message.updatedAt !== message.createdAt">изменено · </template>
            {{ formatTime(message.createdAt) }}
          </span>
        </div>

        <div v-if="isFirstMessageOfDay(index)" class="flex items-center justify-center py-2">
          <span
            class="glass hairline rounded-full px-3.5 py-1 text-xs font-medium text-second shadow-card"
          >
            {{ formatDaySeparator(message.createdAt) }}
          </span>
        </div>
      </template>

      <div v-if="infiniteScroll.isLoading.value" class="py-2 text-center text-sm text-second">
        Загрузка...
      </div>
    </div>

    <div
      v-if="isMuted"
      class="glass hairline-t flex shrink-0 items-center justify-center gap-2 px-4 pt-3 pb-[calc(1.25rem+env(safe-area-inset-bottom))] text-sm text-second lg:px-6 lg:py-4"
    >
      <NavIcon name="mute" :size="16" />
      Вы не можете отправлять сообщения в этом чате
    </div>
    <form
      v-else
      class="glass hairline-t relative flex shrink-0 items-end gap-2.5 px-3 pt-3 pb-[calc(1.25rem+env(safe-area-inset-bottom))] lg:px-5 lg:py-4"
      @submit.prevent="handleSubmit"
    >
      <EmojiPicker :open="emojiPickerOpen" @close="emojiPickerOpen = false" @select="insertEmoji" />

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
        class="glass-field hairline box-border max-h-40 min-h-12 min-w-0 flex-1 resize-none overflow-y-auto rounded-card px-4 py-3 font-sans text-[15px] leading-6 text-main outline-none transition-[border-color,box-shadow] duration-200 placeholder:overflow-hidden placeholder:text-ellipsis placeholder:whitespace-nowrap placeholder:text-second/80 focus-glow"
        @input="handleComposerInput"
        @keydown="handleComposerKeydown"
      />
      <Button
        variant="ghost"
        icon="smile"
        class="mb-1 shrink-0"
        title="Эмодзи"
        aria-label="Эмодзи"
        @click="emojiPickerOpen = !emojiPickerOpen"
      />
      <Button
        type="submit"
        icon="send"
        title="Отправить"
        aria-label="Отправить"
        :disabled="sending || text.trim() === ''"
      />
    </form>

    <div
      v-if="contextMenu"
      class="fixed inset-0 z-40"
      @click="closeContextMenu"
      @contextmenu.prevent="closeContextMenu"
    />

    <div
      v-if="contextMenu"
      class="glass-strong hairline shadow-float fixed z-50 flex w-48 origin-top-left animate-pop flex-col gap-0.5 overflow-hidden rounded-card p-1.5"
      :style="{ top: `${contextMenu.y}px`, left: `${contextMenu.x}px` }"
    >
      <button
        v-if="canEditMessage(contextMenu.message)"
        type="button"
        class="press cursor-pointer rounded-input px-3 py-2 text-left text-sm text-main hover:bg-main/6"
        @click="handleMenuEdit"
      >
        Редактировать
      </button>

      <button
        v-if="canDeleteMessage(contextMenu.message)"
        type="button"
        class="press cursor-pointer rounded-input px-3 py-2 text-left text-sm text-red-600 hover:bg-red-500/12 dark:text-red-400"
        @click="handleMenuDelete"
      >
        Удалить
      </button>
    </div>
  </div>
</template>
