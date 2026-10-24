<script setup lang="ts">
import { computed, defineAsyncComponent, nextTick, onMounted, onUnmounted, ref, watch } from "vue"
import { useRoute } from "vue-router"
import { storeToRefs } from "pinia"
import { useDebounceFn, useInfiniteScroll } from "@vueuse/core"
import { useMessageStore, type MessageItem } from "@/stores/messages"
import { useAuthStore } from "@/stores/auth"
import {
  useChatStore,
  privatePeer,
  type ChatParticipantItem,
  type ChatSummary,
} from "@/stores/chats"
import { useDraftStore } from "@/stores/drafts"
import { EAttachmentKind, EChatType } from "@/graphql/base-types"
import { notify } from "@/lib/notify"
import {
  shortName,
  fullName,
  initials,
  formatTime,
  chatInitials,
  isSameDay,
  formatDaySeparator,
} from "@/lib/format"
import { linkify } from "@/lib/linkify"
import {
  FILE_ACCEPT,
  MEDIA_ACCEPT,
  attachmentKind,
  contentTypeOf,
  formatSize,
  maxSize,
  messagePreview,
} from "@/lib/media"
import { pinForLeave } from "@/lib/transition"
import { isLargeEmojiMessage } from "@/lib/emoji"
import { participantBadges, userBadges } from "@/lib/badges"
import { presenceLabel } from "@/lib/presence"
import { roleLabels } from "@/lib/roles"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import type { AttachmentFieldsFragment } from "@/graphql/fragments/messages.generated"
import Button from "@/components/button.vue"
import Badge from "@/components/badge.vue"
import NavIcon from "@/components/nav-icon.vue"
import Avatar from "@/components/avatar.vue"
import ContextMenu from "@/components/context-menu.vue"
import MediaGrid from "@/components/media-grid.vue"
import AttachmentFiles from "@/components/attachment-files.vue"
import MediaViewer from "@/components/media-viewer.vue"

const EmojiPicker = defineAsyncComponent(() => import("@/components/emoji-picker.vue"))

const PAGE_SIZE = 30
const MAX_ATTACHMENTS = 10

const props = defineProps<{
  chatId: number
  chat?: ChatSummary | null
}>()

const emit = defineEmits<{
  back: []
  "open-info": []
}>()

const route = useRoute()

const messageStore = useMessageStore()
const { messages, totalCount } = storeToRefs(messageStore)

const authStore = useAuthStore()
const { user: currentUser } = storeToRefs(authStore)

const chatStore = useChatStore()
const { chats } = storeToRefs(chatStore)

const peer = computed(() =>
  props.chat && currentUser.value ? privatePeer(props.chat, currentUser.value.id) : null,
)

const peerPresence = computed(() => peer.value?.user ?? null)

const participantsByUserId = computed(() => {
  const chat = chats.value.find((item) => item.id === props.chatId)
  const map = new Map<number, ChatParticipantItem>()
  chat?.participants.forEach((participant) => map.set(participant.user.id, participant))
  return map
})

const participants = computed(() => {
  const chat = chats.value.find((item) => item.id === props.chatId)
  return chat?.participants ?? []
})

const MENTION_PATTERN = /(?:^|\s)@([^\s@]*(?:\s[^\s@]*)?)$/

function mentionLabel(user: UserFieldsFragment) {
  return `@${shortName(user)}`
}

function collectMentionedUserIds(value: string) {
  return participants.value
    .map((participant) => participant.user)
    .filter((user) => user.id !== currentUser.value?.id && value.includes(mentionLabel(user)))
    .map((user) => user.id)
}

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

function canOpenMessageMenu(message: MessageItem) {
  return !isMuted.value || canEditMessage(message) || canDeleteMessage(message)
}

function mediaOf(message: MessageItem) {
  return message.attachments.filter((item) => item.kind !== EAttachmentKind.File)
}

function filesOf(message: MessageItem) {
  return message.attachments.filter((item) => item.kind === EAttachmentKind.File)
}

function isEmojiBubble(message: MessageItem) {
  return (
    message.replyTo === null &&
    message.attachments.length === 0 &&
    isLargeEmojiMessage(message.text)
  )
}

type MessageContextMenu = {
  x: number
  y: number
  message: MessageItem
}

const contextMenu = ref<MessageContextMenu | null>(null)

function closeContextMenu() {
  contextMenu.value = null
}

function handleMessageContextMenu(event: MouseEvent, message: MessageItem) {
  if (!canOpenMessageMenu(message)) {
    return
  }
  event.preventDefault()
  contextMenu.value = {
    x: event.clientX,
    y: event.clientY,
    message,
  }
}

const editingMessageId = ref<number | null>(null)
const editDraft = ref("")
const savingEdit = ref(false)

const replyingTo = ref<MessageItem | null>(null)

function cancelReply() {
  replyingTo.value = null
}

function startReply(message: MessageItem) {
  if (isMuted.value) {
    return
  }
  cancelEdit()
  replyingTo.value = message
  nextTick(() => composerEl.value?.focus())
}

function startEdit(message: MessageItem) {
  cancelReply()
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
    await messageStore.updateMessage(messageId, value, collectMentionedUserIds(value))
    cancelEdit()
  } catch {
    notify.error("Не удалось изменить сообщение")
  } finally {
    savingEdit.value = false
  }
}

function handleMenuReply() {
  const message = contextMenu.value?.message
  closeContextMenu()
  if (message !== undefined) {
    startReply(message)
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
    cancelReply()
  },
)

const draftStore = useDraftStore()

const scrollContainer = ref<HTMLElement | null>(null)
const text = ref(draftStore.getDraft(props.chatId))
const sending = ref(false)

type PendingAttachment = {
  localId: number
  previewUrl: string | null
  name: string
  attachmentId: number | null
}

const fileInputEl = ref<HTMLInputElement | null>(null)
const fileAccept = ref(MEDIA_ACCEPT)
const attachMenuOpen = ref(false)
const pendingAttachments = ref<PendingAttachment[]>([])
let pendingCounter = 0

const isUploading = computed(() =>
  pendingAttachments.value.some((item) => item.attachmentId === null),
)

const readyAttachmentIds = computed(() =>
  pendingAttachments.value
    .map((item) => item.attachmentId)
    .filter((id): id is number => id !== null),
)

const canSubmit = computed(
  () =>
    !sending.value &&
    !isUploading.value &&
    (text.value.trim() !== "" || readyAttachmentIds.value.length > 0),
)

function dropPending(localId: number) {
  const item = pendingAttachments.value.find((pending) => pending.localId === localId)
  if (item?.previewUrl != null) {
    URL.revokeObjectURL(item.previewUrl)
  }
  pendingAttachments.value = pendingAttachments.value.filter(
    (pending) => pending.localId !== localId,
  )
}

function clearPending() {
  pendingAttachments.value.forEach((item) => {
    if (item.previewUrl !== null) {
      URL.revokeObjectURL(item.previewUrl)
    }
  })
  pendingAttachments.value = []
}

async function addFiles(files: File[]) {
  for (const file of files) {
    const kind = attachmentKind(contentTypeOf(file))

    if (file.size > maxSize(kind)) {
      notify.error(`${file.name}: файл больше ${formatSize(maxSize(kind))}`)
      continue
    }

    if (pendingAttachments.value.length >= MAX_ATTACHMENTS) {
      notify.error(`Можно прикрепить не больше ${MAX_ATTACHMENTS} файлов`)
      return
    }

    const localId = (pendingCounter += 1)
    pendingAttachments.value = [
      ...pendingAttachments.value,
      {
        localId,
        previewUrl: kind === EAttachmentKind.File ? null : URL.createObjectURL(file),
        name: file.name,
        attachmentId: null,
      },
    ]

    try {
      const attachmentId = await messageStore.uploadAttachment(props.chatId, file)
      pendingAttachments.value = pendingAttachments.value.map((item) =>
        item.localId === localId ? { ...item, attachmentId } : item,
      )
    } catch (error) {
      dropPending(localId)
      notify.error(error instanceof Error ? error.message : `Не удалось загрузить ${file.name}`)
    }
  }
}

async function pickFiles(accept: string) {
  fileAccept.value = accept
  attachMenuOpen.value = false
  await nextTick()
  fileInputEl.value?.click()
}

async function handleFilePick(event: Event) {
  const input = event.target as HTMLInputElement
  const files = Array.from(input.files ?? [])
  input.value = ""
  await addFiles(files)
}

async function handlePaste(event: ClipboardEvent) {
  const files = Array.from(event.clipboardData?.files ?? [])
  if (files.length === 0) {
    return
  }
  event.preventDefault()
  await addFiles(files)
}

const viewer = ref<{ attachments: AttachmentFieldsFragment[]; index: number } | null>(null)

function openViewer(attachments: AttachmentFieldsFragment[], index: number) {
  viewer.value = { attachments, index }
}

const saveDraft = useDebounceFn((value: string) => {
  draftStore.setDraft(props.chatId, value)
}, 300)

watch(text, (value) => {
  saveDraft(value)
})

onUnmounted(() => {
  draftStore.setDraft(props.chatId, text.value)
  clearPending()
})

const composerEl = ref<HTMLTextAreaElement | null>(null)
const sendsOnEnter = window.matchMedia("(pointer: fine)").matches

const caret = ref(0)
const mentionDismissed = ref(false)
const activeMentionIndex = ref(0)

const mentionQuery = computed(() => {
  if (mentionDismissed.value) {
    return null
  }
  const match = MENTION_PATTERN.exec(text.value.slice(0, caret.value))
  return match === null ? null : (match[1] ?? "")
})

const mentionCandidates = computed(() => {
  const query = mentionQuery.value
  if (query === null) {
    return []
  }

  const normalized = query.trim().toLowerCase()

  return participants.value
    .map((participant) => participant.user)
    .filter((user) => user.id !== currentUser.value?.id)
    .filter((user) => normalized === "" || fullName(user).toLowerCase().includes(normalized))
    .slice(0, 6)
})

function syncCaret() {
  caret.value = composerEl.value?.selectionStart ?? text.value.length
}

function applyMention(user: UserFieldsFragment) {
  const before = text.value.slice(0, caret.value)
  const match = MENTION_PATTERN.exec(before)
  if (match === null) {
    return
  }

  const start = before.length - match[0].length + (match[0].startsWith("@") ? 0 : 1)
  const label = `${mentionLabel(user)} `

  text.value = `${text.value.slice(0, start)}${label}${text.value.slice(caret.value)}`
  mentionDismissed.value = true

  const nextCaret = start + label.length
  nextTick(() => {
    resizeComposer()
    composerEl.value?.focus()
    composerEl.value?.setSelectionRange(nextCaret, nextCaret)
    caret.value = nextCaret
  })
}

function handleMentionKeydown(event: KeyboardEvent) {
  const candidates = mentionCandidates.value
  if (candidates.length === 0) {
    return false
  }

  if (event.key === "ArrowDown") {
    event.preventDefault()
    activeMentionIndex.value = (activeMentionIndex.value + 1) % candidates.length
    return true
  }

  if (event.key === "ArrowUp") {
    event.preventDefault()
    activeMentionIndex.value =
      (activeMentionIndex.value - 1 + candidates.length) % candidates.length
    return true
  }

  if (event.key === "Enter" || event.key === "Tab") {
    const user = candidates[activeMentionIndex.value] ?? candidates[0]
    if (user === undefined) {
      return false
    }
    event.preventDefault()
    applyMention(user)
    return true
  }

  if (event.key === "Escape") {
    event.preventDefault()
    mentionDismissed.value = true
    return true
  }

  return false
}

watch(mentionQuery, () => {
  activeMentionIndex.value = 0
})

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
  mentionDismissed.value = false
  syncCaret()
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
  if (!event.isComposing && handleMentionKeydown(event)) {
    return
  }

  if (event.key === "Escape" && replyingTo.value !== null) {
    event.preventDefault()
    cancelReply()
    return
  }

  if (!sendsOnEnter || event.key !== "Enter" || event.shiftKey || event.isComposing) {
    return
  }

  event.preventDefault()
  handleSubmit()
}

type MessageRow =
  | { kind: "message"; key: string; message: MessageItem }
  | { kind: "day"; key: string; label: string }

const rows = computed(() => {
  const list: MessageRow[] = []

  messages.value.forEach((message, index) => {
    list.push({ kind: "message", key: `message-${message.id}`, message })

    const older = messages.value[index + 1]
    if (older === undefined || !isSameDay(message.createdAt, older.createdAt)) {
      const label = formatDaySeparator(message.createdAt)
      list.push({ kind: "day", key: `day-${label}`, label })
    }
  })

  return list
})

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

const highlightedMessageId = ref<number | null>(null)

async function jumpToMessage(messageId: number) {
  if (!messages.value.some((message) => message.id === messageId)) {
    const position = await messageStore.fetchMessagePosition(messageId)
    if (messages.value.length <= position) {
      await messageStore.fetchMessages(position + 1, 0)
      infiniteScroll.reset()
    }
  }

  await nextTick()

  scrollContainer.value
    ?.querySelector(`[data-message-id="${messageId}"]`)
    ?.scrollIntoView({ block: "center", behavior: "smooth" })

  highlightedMessageId.value = messageId
  setTimeout(() => {
    if (highlightedMessageId.value === messageId) {
      highlightedMessageId.value = null
    }
  }, 2500)
}

function targetMessageId() {
  const raw = route.query.message
  const value = Number(Array.isArray(raw) ? raw[0] : raw)
  return Number.isInteger(value) && value > 0 ? value : null
}

async function openTargetMessage() {
  const messageId = targetMessageId()
  if (messageId === null) {
    return
  }

  try {
    await jumpToMessage(messageId)
  } catch {
    notify.error("Не удалось открыть сообщение")
  }
}

watch(
  () => route.query.message,
  () => {
    openTargetMessage()
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
  await openTargetMessage()
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
  if (!canSubmit.value) {
    return
  }

  const value = text.value.trim()

  sending.value = true
  try {
    await messageStore.sendMessage(
      value,
      collectMentionedUserIds(value),
      replyingTo.value?.id ?? null,
      readyAttachmentIds.value,
    )
    clearPending()
    cancelReply()
    text.value = ""
    mentionDismissed.value = false
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
  <div class="flex h-full w-full min-w-0 flex-1 flex-col">
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
        <Avatar
          :label="chatInitials(chat?.title ?? '')"
          :online="peerPresence?.isOnline ?? false"
        />
        <span class="flex min-w-0 flex-col">
          <span class="truncate text-[15px] font-semibold text-main">{{ chat?.title }}</span>
          <span
            class="truncate text-xs"
            :class="peerPresence?.isOnline ? 'text-green-600 dark:text-green-400' : 'text-second'"
          >
            {{
              chat?.type === EChatType.Public
                ? `${chat.participants.length} участников`
                : peerPresence !== null
                  ? presenceLabel(peerPresence)
                  : "Личный чат"
            }}
          </span>
        </span>
      </button>
    </div>

    <div
      ref="scrollContainer"
      class="relative flex flex-1 flex-col-reverse gap-3 overflow-y-auto px-4 py-3 lg:px-6 lg:py-4"
    >
      <TransitionGroup name="msg" @before-leave="pinForLeave">
        <div
          v-for="row in rows"
          :key="row.key"
          v-bind="row.kind === 'message' ? { 'data-message-id': row.message.id } : {}"
          class="group flex flex-col gap-1 rounded-card transition-colors duration-500"
          :class="
            row.kind === 'day'
              ? 'items-center py-2'
              : [
                  highlightedMessageId === row.message.id
                    ? 'bg-accent/10 ring-1 ring-accent/30'
                    : '',
                  row.message.user.id === currentUser?.id
                    ? 'origin-bottom-right items-end'
                    : 'origin-bottom-left items-start',
                  canOpenMessageMenu(row.message) ? 'cursor-context-menu' : '',
                ]
          "
          @contextmenu="row.kind === 'message' && handleMessageContextMenu($event, row.message)"
          @dblclick.prevent="row.kind === 'message' && startReply(row.message)"
        >
          <span
            v-if="row.kind === 'day'"
            class="glass hairline rounded-full px-3.5 py-1 text-xs font-medium text-second shadow-card"
          >
            {{ row.label }}
          </span>

          <template v-else>
            <div
              class="flex w-full items-center gap-1.5"
              :class="row.message.user.id === currentUser?.id ? 'flex-row-reverse' : 'flex-row'"
            >
              <Transition name="swap" mode="out-in">
                <div
                  v-if="editingMessageId === row.message.id"
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
                    isEmojiBubble(row.message)
                      ? 'px-1 py-0.5 text-5xl leading-tight'
                      : 'px-4 py-2.5 text-[15px]',
                    isEmojiBubble(row.message)
                      ? 'text-main'
                      : row.message.user.id === currentUser?.id
                        ? 'accent-surface glow-accent bubble-own text-bg'
                        : 'glass hairline shadow-card bubble-other text-main',
                  ]"
                >
                  <div
                    v-if="row.message.user.id !== currentUser?.id"
                    class="mb-1 flex flex-wrap items-center gap-1.5 text-xs font-medium opacity-70"
                  >
                    <span>{{ shortName(row.message.user) }}</span>
                    <Badge
                      v-for="badge in badgesForSender(row.message.user)"
                      :key="badge.label"
                      :variant="badge.variant"
                      :label="badge.label"
                    />
                  </div>
                  <button
                    v-if="row.message.replyTo !== null"
                    type="button"
                    class="press mb-1.5 flex w-full cursor-pointer flex-col items-start gap-0.5 rounded-input border-l-2 border-current/40 bg-current/8 px-2 py-1 text-left opacity-80 transition-opacity hover:opacity-100"
                    @click.stop="jumpToMessage(row.message.replyTo.id)"
                    @dblclick.stop
                  >
                    <span class="w-full truncate text-xs font-semibold">
                      {{ shortName(row.message.replyTo.user) }}
                    </span>
                    <span class="line-clamp-2 break-words text-xs">
                      {{ row.message.replyTo.text || "Вложение" }}
                    </span>
                  </button>

                  <MediaGrid
                    :attachments="mediaOf(row.message)"
                    @open="openViewer(mediaOf(row.message), $event)"
                  />
                  <AttachmentFiles :attachments="filesOf(row.message)" />

                  <div v-if="row.message.text !== ''" class="whitespace-pre-wrap break-words">
                    <template
                      v-for="(segment, segmentIndex) in linkify(row.message.text)"
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
              </Transition>

              <button
                v-if="!isMuted && editingMessageId !== row.message.id"
                type="button"
                class="press glass hairline flex h-7 w-7 shrink-0 cursor-pointer items-center justify-center rounded-full text-second opacity-100 transition-opacity hover:text-main lg:opacity-0 lg:group-hover:opacity-100"
                title="Ответить"
                aria-label="Ответить"
                @click.stop="startReply(row.message)"
                @dblclick.stop
              >
                <NavIcon name="reply" :size="14" />
              </button>
            </div>

            <span class="flex items-center gap-1 px-1.5 text-xs text-second/80">
              <template v-if="row.message.updatedAt !== row.message.createdAt">
                изменено ·
              </template>
              {{ formatTime(row.message.createdAt) }}
            </span>
          </template>
        </div>
      </TransitionGroup>

      <Transition name="fade">
        <div v-if="infiniteScroll.isLoading.value" class="py-2 text-center text-sm text-second">
          Загрузка...
        </div>
      </Transition>
    </div>

    <div
      v-if="replyingTo !== null && !isMuted"
      class="glass hairline-t flex shrink-0 items-center gap-2.5 px-3 py-2 lg:px-5"
    >
      <NavIcon name="reply" :size="16" class="text-accent" />
      <div class="min-w-0 flex-1 border-l-2 border-accent/50 pl-2">
        <div class="truncate text-xs font-semibold text-accent">
          {{ shortName(replyingTo.user) }}
        </div>
        <div class="truncate text-xs text-second">
          {{ messagePreview(replyingTo) }}
        </div>
      </div>
      <button
        type="button"
        class="press flex h-7 w-7 shrink-0 cursor-pointer items-center justify-center rounded-full text-second hover:bg-main/6 hover:text-main"
        title="Отменить ответ"
        aria-label="Отменить ответ"
        @click="cancelReply"
      >
        <NavIcon name="cancel" :size="14" />
      </button>
    </div>

    <div
      v-if="isMuted"
      class="glass hairline-t flex shrink-0 items-center justify-center gap-2 px-4 pt-3 pb-[calc(1.25rem+env(safe-area-inset-bottom))] text-sm text-second lg:px-6 lg:py-4"
    >
      <NavIcon name="mute" :size="16" />
      Вы не можете отправлять сообщения в этом чате
    </div>
    <div
      v-else-if="pendingAttachments.length > 0"
      class="glass hairline-t flex shrink-0 gap-2 overflow-x-auto px-3 py-2 lg:px-5"
    >
      <div
        v-for="item in pendingAttachments"
        :key="item.localId"
        class="relative h-16 w-16 shrink-0 overflow-hidden rounded-input bg-black/15"
      >
        <img
          v-if="item.previewUrl !== null"
          :src="item.previewUrl"
          :alt="item.name"
          class="h-full w-full object-cover"
        />
        <span
          v-else
          class="flex h-full w-full flex-col items-center justify-center gap-1 px-1 text-second"
          :title="item.name"
        >
          <NavIcon name="file" :size="18" />
          <span class="w-full truncate text-center text-[10px]">{{ item.name }}</span>
        </span>
        <span
          v-if="item.attachmentId === null"
          class="absolute inset-0 flex items-center justify-center bg-black/45 text-[10px] font-medium text-white"
        >
          Загрузка
        </span>
        <button
          type="button"
          class="press absolute top-0.5 right-0.5 flex h-5 w-5 cursor-pointer items-center justify-center rounded-full bg-black/60 text-white hover:bg-black/80"
          title="Убрать"
          aria-label="Убрать вложение"
          @click="dropPending(item.localId)"
        >
          <NavIcon name="cancel" :size="12" />
        </button>
      </div>
    </div>

    <form
      v-if="!isMuted"
      class="glass hairline-t relative flex shrink-0 items-end gap-2.5 px-3 pt-3 pb-[calc(1.25rem+env(safe-area-inset-bottom))] lg:px-5 lg:py-4"
      @submit.prevent="handleSubmit"
    >
      <EmojiPicker
        v-if="emojiPickerOpen"
        :open="emojiPickerOpen"
        @close="emojiPickerOpen = false"
        @select="insertEmoji"
      />

      <div
        v-if="mentionCandidates.length > 0"
        class="glass-strong hairline shadow-float absolute bottom-[calc(100%-0.5rem)] left-3 z-20 flex w-[min(20rem,calc(100%-1.5rem))] flex-col gap-0.5 rounded-card p-1.5 lg:left-5"
      >
        <button
          v-for="(candidate, candidateIndex) in mentionCandidates"
          :key="candidate.id"
          type="button"
          class="press flex cursor-pointer items-center gap-2.5 rounded-input px-2.5 py-2 text-left"
          :class="
            candidateIndex === activeMentionIndex
              ? 'bg-accent/12 text-main'
              : 'text-second hover:bg-main/6 hover:text-main'
          "
          @mousedown.prevent="applyMention(candidate)"
        >
          <Avatar :label="initials(candidate)" size="sm" />
          <span class="flex min-w-0 flex-col">
            <span class="truncate text-sm font-medium text-main">{{ shortName(candidate) }}</span>
            <span class="truncate text-xs text-second">{{ roleLabels[candidate.role] }}</span>
          </span>
        </button>
      </div>

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
        @paste="handlePaste"
        @keydown="handleComposerKeydown"
        @keyup="syncCaret"
        @click="syncCaret"
      />
      <div v-if="attachMenuOpen" class="fixed inset-0 z-40" @click="attachMenuOpen = false" />
      <div
        v-if="attachMenuOpen"
        class="glass-strong hairline shadow-float absolute right-3 bottom-full z-50 mb-3 flex w-52 origin-bottom-right animate-pop flex-col gap-0.5 rounded-card p-1.5 lg:right-5"
      >
        <button
          type="button"
          class="press flex cursor-pointer items-center gap-2.5 rounded-input px-2.5 py-2 text-left text-sm text-main hover:bg-main/6"
          @click="pickFiles(MEDIA_ACCEPT)"
        >
          <NavIcon name="image" :size="16" class="text-second" />
          Фото или видео
        </button>
        <button
          type="button"
          class="press flex cursor-pointer items-center gap-2.5 rounded-input px-2.5 py-2 text-left text-sm text-main hover:bg-main/6"
          @click="pickFiles(FILE_ACCEPT)"
        >
          <NavIcon name="file" :size="16" class="text-second" />
          Файл
        </button>
      </div>

      <input
        ref="fileInputEl"
        type="file"
        multiple
        :accept="fileAccept"
        class="hidden"
        @change="handleFilePick"
      />
      <Button
        variant="ghost"
        icon="clip"
        class="mb-1 shrink-0"
        title="Прикрепить"
        aria-label="Прикрепить"
        @click="attachMenuOpen = !attachMenuOpen"
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
        :disabled="!canSubmit"
      />
    </form>

    <ContextMenu
      v-if="contextMenu"
      :x="contextMenu.x"
      :y="contextMenu.y"
      class="w-48"
      @close="closeContextMenu"
    >
      <button
        v-if="!isMuted"
        type="button"
        class="press cursor-pointer rounded-input px-3 py-2 text-left text-sm text-main hover:bg-main/6"
        @click="handleMenuReply"
      >
        Ответить
      </button>

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
    </ContextMenu>

    <MediaViewer
      v-if="viewer !== null"
      :attachments="viewer.attachments"
      :index="viewer.index"
      @close="viewer = null"
    />
  </div>
</template>
