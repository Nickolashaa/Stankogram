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
import Avatar from "@/components/avatar.vue"

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

const searchQuery = ref("")
const startingUserId = ref<number | null>(null)

watch(
  () => props.open,
  (isOpen) => {
    if (!isOpen) {
      return
    }
    searchQuery.value = ""
    startingUserId.value = null
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
  users.value.filter((user) => user.id !== currentUser.value?.id),
)

function handleClose() {
  emit("close")
}

async function startChat(user: UserFieldsFragment) {
  if (startingUserId.value !== null) {
    return
  }

  startingUserId.value = user.id
  try {
    const chatId = await chatStore.startPrivateChat(user.id)
    emit("created", chatId)
  } catch {
    notify.error("Не удалось открыть чат")
  } finally {
    startingUserId.value = null
  }
}
</script>

<template>
  <div
    v-if="open"
    class="fixed inset-0 z-50 flex animate-appear items-start justify-center bg-black/40 p-4 sm:items-center"
    @click.self="handleClose"
  >
    <div
      class="flex max-h-[calc(100dvh-2rem)] sm:max-h-[85vh] w-full max-w-md flex-col gap-5 overflow-y-auto rounded-card bg-card p-5 shadow-card sm:p-8"
    >
      <div class="flex items-center justify-between gap-4">
        <h2 class="m-0 text-xl font-semibold text-main">Личный чат</h2>
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
        <Input v-model="searchQuery" placeholder="Имя, фамилия, email..." autofocus />

        <div
          v-if="searchQuery.trim() !== ''"
          class="flex max-h-56 flex-col overflow-y-auto rounded-input border-[1.5px] border-second/20"
        >
          <button
            v-for="user in searchResults"
            :key="user.id"
            type="button"
            class="flex w-full cursor-pointer items-center gap-3 px-3 py-2.5 text-left transition-colors duration-150 hover:bg-accent/5 disabled:cursor-not-allowed disabled:opacity-60"
            :disabled="startingUserId !== null"
            @click="startChat(user)"
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

      <Button variant="ghost" icon="cancel" :short-mode="false" @click="handleClose">
        Отмена
      </Button>
    </div>
  </div>
</template>
