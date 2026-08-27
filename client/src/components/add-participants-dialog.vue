<script setup lang="ts">
import { computed, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import { useUserStore } from "@/stores/users"
import { useChatStore } from "@/stores/chats"
import { notify } from "@/lib/notify"
import { fullName, initials } from "@/lib/format"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import Input from "@/components/input.vue"
import Button from "@/components/button.vue"
import NavIcon from "@/components/nav-icon.vue"
import Avatar from "@/components/avatar.vue"

const SEARCH_PAGE_SIZE = 20

const props = defineProps<{
  open: boolean
  chatId: number
  existingUserIds: number[]
}>()

const emit = defineEmits<{
  close: []
  added: []
}>()

const userStore = useUserStore()
const chatStore = useChatStore()
const { users } = storeToRefs(userStore)

const searchQuery = ref("")
const selectedUsers = ref<UserFieldsFragment[]>([])
const submitting = ref(false)

watch(
  () => props.open,
  (isOpen) => {
    if (!isOpen) {
      return
    }
    searchQuery.value = ""
    selectedUsers.value = []
    users.value = []
  },
)

watch(searchQuery, async (value) => {
  const trimmed = value.trim()
  if (trimmed === "") {
    users.value = []
    return
  }
  await userStore.fetchUsers({ searchQuery: trimmed }, SEARCH_PAGE_SIZE, 0)
})

const searchResults = computed(() =>
  users.value.filter((user) => !props.existingUserIds.includes(user.id) && !isSelected(user)),
)

const canSubmit = computed(() => selectedUsers.value.length > 0 && !submitting.value)

function isSelected(user: UserFieldsFragment) {
  return selectedUsers.value.some((item) => item.id === user.id)
}

function selectUser(user: UserFieldsFragment) {
  selectedUsers.value = [...selectedUsers.value, user]
}

function unselectUser(user: UserFieldsFragment) {
  selectedUsers.value = selectedUsers.value.filter((item) => item.id !== user.id)
}

function handleClose() {
  emit("close")
}

async function handleSubmit() {
  if (!canSubmit.value) {
    return
  }

  submitting.value = true
  try {
    for (const user of selectedUsers.value) {
      await chatStore.addParticipant(props.chatId, user.id)
    }
    notify.success("Участники добавлены")
    emit("added")
  } catch {
    notify.error("Не удалось добавить участников")
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div
    v-if="open"
    class="fixed inset-0 z-50 flex animate-appear items-center justify-center bg-black/40 px-4"
    @click.self="handleClose"
  >
    <form
      class="flex max-h-[85vh] w-full max-w-md flex-col gap-5 overflow-y-auto rounded-card bg-card p-5 shadow-card sm:p-8"
      @submit.prevent="handleSubmit"
    >
      <div class="flex items-center justify-between gap-4">
        <h2 class="m-0 text-xl font-semibold text-main">Добавить участников</h2>
        <button
          type="button"
          class="cursor-pointer text-second transition-colors duration-150 hover:text-main"
          aria-label="Закрыть"
          @click="handleClose"
        >
          <NavIcon name="cancel" />
        </button>
      </div>

      <div class="flex min-h-0 flex-1 flex-col gap-3">
        <div v-if="selectedUsers.length > 0" class="flex flex-wrap gap-2">
          <span
            v-for="user in selectedUsers"
            :key="user.id"
            class="flex items-center gap-1.5 rounded-full bg-accent/10 py-1 pr-1.5 pl-1 text-sm text-main"
          >
            <span
              class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-accent text-[11px] font-semibold text-bg"
            >
              {{ initials(user) }}
            </span>
            {{ fullName(user) }}
            <button
              type="button"
              class="flex h-4 w-4 cursor-pointer items-center justify-center rounded-full text-accent/70 transition-colors duration-150 hover:bg-accent/20 hover:text-accent"
              aria-label="Убрать участника"
              @click="unselectUser(user)"
            >
              ×
            </button>
          </span>
        </div>

        <Input v-model="searchQuery" placeholder="Найти участников..." />

        <div
          v-if="searchQuery.trim() !== ''"
          class="flex max-h-56 flex-col overflow-y-auto rounded-input border-[1.5px] border-second/20"
        >
          <button
            v-for="user in searchResults"
            :key="user.id"
            type="button"
            class="flex w-full cursor-pointer items-center gap-3 px-3 py-2.5 text-left transition-colors duration-150 hover:bg-accent/5"
            @click="selectUser(user)"
          >
            <Avatar :label="initials(user)" size="sm" />
            <span class="flex flex-col gap-0.5 overflow-hidden">
              <span class="truncate text-[15px] font-medium text-main">{{ fullName(user) }}</span>
              <span class="truncate text-xs text-second">{{ user.email }}</span>
            </span>
          </button>

          <div v-if="searchResults.length === 0" class="px-3 py-4 text-center text-sm text-second">
            Никого не найдено
          </div>
        </div>
      </div>

      <div class="mt-1 flex gap-2">
        <Button
          type="button"
          variant="ghost"
          class="flex-1"
          icon="cancel"
          :short-mode="false"
          @click="handleClose"
        >
          Отмена
        </Button>
        <Button
          type="submit"
          class="flex-[2]"
          icon="plus"
          :short-mode="false"
          :disabled="!canSubmit"
        >
          Добавить
        </Button>
      </div>
    </form>
  </div>
</template>
