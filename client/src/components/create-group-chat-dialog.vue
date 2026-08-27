<script setup lang="ts">
import { computed, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import { useUserStore } from "@/stores/users"
import { useAuthStore } from "@/stores/auth"
import { useChatStore } from "@/stores/chats"
import { notify } from "@/lib/notify"
import { fullName, initials } from "@/lib/format"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import Input from "@/components/input.vue"
import Button from "@/components/button.vue"
import NavIcon from "@/components/nav-icon.vue"

const SEARCH_PAGE_SIZE = 20

const props = defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  close: []
  created: [chatId: number]
}>()

const userStore = useUserStore()
const authStore = useAuthStore()
const chatStore = useChatStore()
const { users } = storeToRefs(userStore)
const { user: currentUser } = storeToRefs(authStore)

const title = ref("")
const searchQuery = ref("")
const selectedUsers = ref<UserFieldsFragment[]>([])
const submitting = ref(false)

watch(
  () => props.open,
  (isOpen) => {
    if (!isOpen) {
      return
    }
    title.value = ""
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
  users.value.filter((user) => user.id !== currentUser.value?.id && !isSelected(user)),
)

const canSubmit = computed(() => title.value.trim() !== "" && !submitting.value)

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
    const chatId = await chatStore.createGroupChat(
      title.value.trim(),
      selectedUsers.value.map((user) => user.id),
    )
    notify.success("Групповой чат создан")
    emit("created", chatId)
  } catch {
    notify.error("Не удалось создать групповой чат")
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
      class="flex max-h-[85vh] w-full max-w-md flex-col gap-5 rounded-card bg-card p-8 shadow-card"
      @submit.prevent="handleSubmit"
    >
      <div class="flex items-center justify-between gap-4">
        <h2 class="m-0 text-xl font-semibold text-main">Новая группа</h2>
        <button
          type="button"
          class="cursor-pointer text-second transition-colors duration-150 hover:text-main"
          aria-label="Закрыть"
          @click="handleClose"
        >
          <NavIcon name="cancel" />
        </button>
      </div>

      <Input v-model="title" placeholder="Название группы" />

      <div class="flex min-h-0 flex-1 flex-col gap-3">
        <span class="text-xs font-medium uppercase tracking-wide text-second">
          Участники{{ selectedUsers.length > 0 ? ` (${selectedUsers.length})` : "" }}
        </span>

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
          class="flex max-h-48 flex-col overflow-y-auto rounded-input border-[1.5px] border-second/20"
        >
          <button
            v-for="user in searchResults"
            :key="user.id"
            type="button"
            class="flex w-full cursor-pointer items-center gap-3 px-3 py-2.5 text-left transition-colors duration-150 hover:bg-accent/5"
            @click="selectUser(user)"
          >
            <span
              class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-second/15 text-xs font-semibold text-second"
            >
              {{ initials(user) }}
            </span>
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
          Создать
        </Button>
      </div>
    </form>
  </div>
</template>
