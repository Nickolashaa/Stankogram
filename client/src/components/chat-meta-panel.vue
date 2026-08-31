<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import type { ChatSummary, ChatParticipantItem } from "@/stores/chats"
import { useAuthStore } from "@/stores/auth"
import { useChatStore } from "@/stores/chats"
import { EChatType } from "@/graphql/base-types"
import { fullName, chatInitials, initials } from "@/lib/format"
import { participantBadges } from "@/lib/badges"
import { notify } from "@/lib/notify"
import Badge from "@/components/badge.vue"
import Button from "@/components/button.vue"
import NavIcon from "@/components/nav-icon.vue"
import Avatar from "@/components/avatar.vue"
import AddParticipantsDialog from "@/components/add-participants-dialog.vue"

const props = withDefaults(
  defineProps<{
    chat: ChatSummary
    manage?: boolean
    variant?: "sidebar" | "page"
  }>(),
  {
    manage: false,
    variant: "sidebar",
  },
)

const emit = defineEmits<{ left: []; deleted: [] }>()

const chatTypeLabels: Record<EChatType, string> = {
  [EChatType.Private]: "Личный чат",
  [EChatType.Public]: "Групповой чат",
}

const authStore = useAuthStore()
const chatStore = useChatStore()
const { user: currentUser } = storeToRefs(authStore)

const isGroupChat = computed(() => props.chat.type === EChatType.Public)

const currentParticipant = computed(
  () => props.chat.participants.find((item) => item.user.id === currentUser.value?.id) ?? null,
)

const isCurrentUserAdmin = computed(
  () => isGroupChat.value && (props.manage || currentParticipant.value?.isAdmin === true),
)

const editingTitle = ref(false)
const titleDraft = ref("")
const savingTitle = ref(false)

function startEditTitle() {
  titleDraft.value = props.chat.title
  editingTitle.value = true
}

function cancelEditTitle() {
  editingTitle.value = false
}

async function saveTitle() {
  const value = titleDraft.value.trim()
  if (value === "" || value === props.chat.title) {
    editingTitle.value = false
    return
  }

  savingTitle.value = true
  try {
    await chatStore.updateChatTitle(props.chat.id, value)
    editingTitle.value = false
  } catch {
    notify.error("Не удалось обновить название чата")
  } finally {
    savingTitle.value = false
  }
}

async function toggleAdmin(participant: ChatParticipantItem) {
  try {
    await chatStore.setParticipantPermissions(
      props.chat.id,
      participant.user.id,
      !participant.isAdmin,
      participant.isMuted,
    )
  } catch {
    notify.error("Не удалось изменить права участника")
  }
}

async function toggleMute(participant: ChatParticipantItem) {
  try {
    await chatStore.setParticipantPermissions(
      props.chat.id,
      participant.user.id,
      participant.isAdmin,
      !participant.isMuted,
    )
  } catch {
    notify.error("Не удалось изменить статус участника")
  }
}

async function removeParticipant(participant: ChatParticipantItem) {
  if (!window.confirm(`Удалить ${fullName(participant.user)} из чата?`)) {
    return
  }

  try {
    await chatStore.removeParticipant(props.chat.id, participant.user.id)
    notify.success("Участник удалён из чата")
  } catch {
    notify.error("Не удалось удалить участника")
  }
}

const canLeave = computed(
  () => !props.manage && isGroupChat.value && currentParticipant.value !== null,
)

const leaving = ref(false)

async function leaveChat() {
  if (!window.confirm(`Выйти из чата «${props.chat.title}»?`)) {
    return
  }

  leaving.value = true
  try {
    await chatStore.leaveChat(props.chat.id)
    notify.success("Вы вышли из чата")
    emit("left")
  } catch {
    notify.error("Не удалось выйти из чата")
  } finally {
    leaving.value = false
  }
}

const canDelete = computed(() => props.manage && isGroupChat.value)

const deleting = ref(false)

async function deleteChat() {
  if (!window.confirm(`Удалить чат «${props.chat.title}» вместе со всеми сообщениями?`)) {
    return
  }

  deleting.value = true
  try {
    await chatStore.deleteChat(props.chat.id)
    notify.success("Чат удалён")
    emit("deleted")
  } catch {
    notify.error("Не удалось удалить чат")
  } finally {
    deleting.value = false
  }
}

const addParticipantsOpen = ref(false)

type ParticipantContextMenu = {
  x: number
  y: number
  participant: ChatParticipantItem
}

const MENU_WIDTH = 224
const MENU_HEIGHT = 140

const contextMenu = ref<ParticipantContextMenu | null>(null)

function closeContextMenu() {
  contextMenu.value = null
}

function handleContextMenu(event: MouseEvent, participant: ChatParticipantItem) {
  if (!isCurrentUserAdmin.value) {
    return
  }
  event.preventDefault()
  contextMenu.value = {
    x: Math.min(event.clientX, window.innerWidth - MENU_WIDTH - 8),
    y: Math.min(event.clientY, window.innerHeight - MENU_HEIGHT - 8),
    participant,
  }
}

async function handleMenuToggleAdmin() {
  const participant = contextMenu.value?.participant
  closeContextMenu()
  if (participant !== undefined) {
    await toggleAdmin(participant)
  }
}

async function handleMenuToggleMute() {
  const participant = contextMenu.value?.participant
  closeContextMenu()
  if (participant !== undefined) {
    await toggleMute(participant)
  }
}

async function handleMenuRemove() {
  const participant = contextMenu.value?.participant
  closeContextMenu()
  if (participant !== undefined) {
    await removeParticipant(participant)
  }
}

watch(
  () => props.chat.id,
  () => closeContextMenu(),
)

function handleEscape(event: KeyboardEvent) {
  if (event.key === "Escape") {
    closeContextMenu()
  }
}

onMounted(() => window.addEventListener("keydown", handleEscape))
onUnmounted(() => window.removeEventListener("keydown", handleEscape))
</script>

<template>
  <div
    class="flex h-full w-full flex-col overflow-y-auto bg-card"
    :class="
      variant === 'page'
        ? 'flex-1 rounded-card shadow-card'
        : 'lg:w-80 lg:shrink-0 lg:border-l lg:border-second/15'
    "
  >
    <div class="flex items-center gap-3 border-b border-second/15 px-4 py-5 lg:px-6 lg:py-6">
      <Avatar :label="chatInitials(chat.title)" size="lg" />

      <div class="flex min-w-0 flex-1 flex-col gap-1">
        <div class="flex items-center gap-2">
          <template v-if="editingTitle">
            <input
              v-model="titleDraft"
              autofocus
              class="h-9 min-w-0 flex-1 rounded-input border-[1.5px] border-second/30 bg-bg px-3 text-[15px] font-semibold text-main outline-none transition-colors duration-150 focus:border-accent"
              @keyup.enter="saveTitle"
              @keyup.esc="cancelEditTitle"
            />
            <Button
              variant="ghost"
              icon="save"
              class="!text-accent hover:!text-accent-hover"
              title="Сохранить"
              aria-label="Сохранить"
              :disabled="savingTitle"
              @click="saveTitle"
            />
            <Button
              variant="ghost"
              icon="cancel"
              title="Отмена"
              aria-label="Отмена"
              @click="cancelEditTitle"
            />
          </template>
          <template v-else>
            <h2 class="m-0 min-w-0 flex-1 truncate text-lg font-semibold text-main">
              {{ chat.title }}
            </h2>
            <Button
              v-if="isCurrentUserAdmin"
              variant="ghost"
              icon="edit"
              title="Изменить название"
              aria-label="Изменить название"
              @click="startEditTitle"
            />
          </template>
        </div>
        <span class="text-sm text-second">{{ chatTypeLabels[chat.type] }}</span>
      </div>
    </div>

    <div class="flex flex-col gap-3 px-4 py-5 lg:px-6">
      <div class="flex items-center justify-between gap-2">
        <span class="text-xs font-medium uppercase tracking-wide text-second">
          Участники ({{ chat.participants.length }})
        </span>
        <button
          v-if="isCurrentUserAdmin"
          type="button"
          class="flex cursor-pointer items-center gap-1 text-xs font-medium text-accent transition-colors duration-150 hover:text-accent-hover"
          @click="addParticipantsOpen = true"
        >
          <NavIcon name="plus" :size="14" />
          Добавить
        </button>
      </div>

      <div class="flex flex-col gap-1">
        <div
          v-for="participant in chat.participants"
          :key="participant.id"
          class="flex items-center gap-3 rounded-card px-2 py-2.5 transition-colors duration-150"
          :class="isCurrentUserAdmin ? 'cursor-context-menu hover:bg-accent/5' : ''"
          @contextmenu="handleContextMenu($event, participant)"
        >
          <Avatar :label="initials(participant.user)" size="sm" />
          <div class="flex min-w-0 flex-1 flex-col gap-1.5">
            <span class="truncate text-[15px] font-medium text-main">
              {{ fullName(participant.user) }}
            </span>
            <div class="flex flex-wrap gap-1.5">
              <Badge
                v-for="badge in participantBadges(participant.user, participant)"
                :key="badge.label"
                :variant="badge.variant"
                :label="badge.label"
              />
            </div>
          </div>
        </div>
      </div>

      <span v-if="isCurrentUserAdmin" class="text-xs text-second">
        Нажмите правой кнопкой мыши на участника, чтобы изменить его права
      </span>
    </div>

    <div v-if="canLeave || canDelete" class="mt-auto border-t border-second/15 px-4 py-4 lg:px-6">
      <button
        v-if="canLeave"
        type="button"
        class="flex w-full cursor-pointer items-center justify-center gap-2 rounded-input border-[1.5px] border-red-500/30 px-4 py-2.5 text-sm font-medium text-red-600 transition-colors duration-150 hover:bg-red-500/10 disabled:cursor-not-allowed disabled:opacity-60 dark:text-red-400"
        :disabled="leaving"
        @click="leaveChat"
      >
        <NavIcon name="logout" :size="16" />
        Выйти из чата
      </button>

      <button
        v-if="canDelete"
        type="button"
        class="flex w-full cursor-pointer items-center justify-center gap-2 rounded-input border-[1.5px] border-red-500/30 px-4 py-2.5 text-sm font-medium text-red-600 transition-colors duration-150 hover:bg-red-500/10 disabled:cursor-not-allowed disabled:opacity-60 dark:text-red-400"
        :disabled="deleting"
        @click="deleteChat"
      >
        <NavIcon name="delete" :size="16" />
        Удалить чат
      </button>
    </div>

    <AddParticipantsDialog
      :open="addParticipantsOpen"
      :chat-id="chat.id"
      :existing-user-ids="chat.participants.map((participant) => participant.user.id)"
      @close="addParticipantsOpen = false"
      @added="addParticipantsOpen = false"
    />

    <div
      v-if="contextMenu"
      class="fixed inset-0 z-40"
      @click="closeContextMenu"
      @contextmenu.prevent="closeContextMenu"
    />

    <div
      v-if="contextMenu"
      class="fixed z-50 flex w-56 animate-appear flex-col overflow-hidden rounded-input border-[1.5px] border-second/15 bg-card py-1.5 shadow-card"
      :style="{ top: `${contextMenu.y}px`, left: `${contextMenu.x}px` }"
    >
      <span class="truncate px-4 pt-1 pb-2 text-xs font-medium text-second">
        {{ fullName(contextMenu.participant.user) }}
      </span>

      <button
        type="button"
        class="cursor-pointer px-4 py-2 text-left text-sm text-main transition-colors duration-150 hover:bg-accent/10"
        @click="handleMenuToggleAdmin"
      >
        {{ contextMenu.participant.isAdmin ? "Разжаловать" : "Сделать админом" }}
      </button>

      <button
        type="button"
        class="cursor-pointer px-4 py-2 text-left text-sm text-main transition-colors duration-150 hover:bg-accent/10"
        @click="handleMenuToggleMute"
      >
        {{ contextMenu.participant.isMuted ? "Размутить" : "Замутить" }}
      </button>

      <button
        type="button"
        class="cursor-pointer px-4 py-2 text-left text-sm text-red-600 transition-colors duration-150 hover:bg-red-500/10 dark:text-red-400"
        @click="handleMenuRemove"
      >
        Удалить из чата
      </button>
    </div>
  </div>
</template>
