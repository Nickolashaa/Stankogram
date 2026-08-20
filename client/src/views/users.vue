<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import { useRouter } from "vue-router"
import { useUserStore } from "@/stores/users"
import { useChatStore } from "@/stores/chats"
import { useAuthStore } from "@/stores/auth"
import { roleLabels } from "@/lib/roles"
import { notify } from "@/lib/notify"
import type { components } from "@/api/schema"
import Input from "@/components/input.vue"

type UserResponse = components["schemas"]["UserResponse"]

const router = useRouter()
const userStore = useUserStore()
const chatStore = useChatStore()
const authStore = useAuthStore()
const { users } = storeToRefs(userStore)
const { user: currentUser } = storeToRefs(authStore)

const searchQuery = ref("")
const openingUserId = ref<number | null>(null)

const otherUsers = computed(() => users.value.filter((user) => user.id !== currentUser.value?.id))

async function fetchUsers() {
  await userStore.fetchUsers(
    { search_query: searchQuery.value.trim() === "" ? undefined : searchQuery.value.trim() },
    50,
    0,
  )
}

watch(searchQuery, fetchUsers)

onMounted(fetchUsers)

function fullName(user: UserResponse) {
  return [user.surname, user.name, user.patronymic].filter(Boolean).join(" ")
}

async function openChat(user: UserResponse) {
  openingUserId.value = user.id
  try {
    const chat = await chatStore.getOrCreatePrivateChat(user.id)
    router.push({ path: "/chats", query: { chat: chat.chat.id } })
  } catch {
    notify.error("Не удалось открыть чат")
  } finally {
    openingUserId.value = null
  }
}
</script>

<template>
  <div class="flex animate-appear flex-col gap-6 p-10">
    <h1 class="m-0 text-2xl font-semibold text-main">Пользователи</h1>

    <Input v-model="searchQuery" placeholder="Имя, фамилия, email..." />

    <div class="flex flex-col gap-2">
      <button
        v-for="user in otherUsers"
        :key="user.id"
        type="button"
        class="flex cursor-pointer items-center justify-between gap-4 rounded-card bg-card px-5 py-4 text-left shadow-card transition-colors duration-150 hover:bg-accent/5 disabled:cursor-not-allowed disabled:opacity-60"
        :disabled="openingUserId === user.id"
        @click="openChat(user)"
      >
        <div class="flex flex-col gap-1">
          <span class="text-[15px] font-medium text-main">{{ fullName(user) }}</span>
          <span class="text-sm text-second">{{ user.email }}</span>
        </div>
        <span class="text-sm text-second">{{ roleLabels[user.role] }}</span>
      </button>

      <div v-if="otherUsers.length === 0" class="px-5 py-8 text-center text-second">
        Пользователи не найдены
      </div>
    </div>
  </div>
</template>
