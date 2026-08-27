<script setup lang="ts">
import { computed, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import { useRouter } from "vue-router"
import { useInfiniteScroll } from "@vueuse/core"
import { useUserStore } from "@/stores/users"
import { useAuthStore } from "@/stores/auth"
import { useChatStore } from "@/stores/chats"
import { fullName } from "@/lib/format"
import { userBadges } from "@/lib/badges"
import { notify } from "@/lib/notify"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import Input from "@/components/input.vue"
import Button from "@/components/button.vue"
import Badge from "@/components/badge.vue"

const PAGE_SIZE = 50

const router = useRouter()
const userStore = useUserStore()
const authStore = useAuthStore()
const chatStore = useChatStore()
const { users, totalCount } = storeToRefs(userStore)
const { user: currentUser } = storeToRefs(authStore)

const searchQuery = ref("")
const startingChatWithUserId = ref<number | null>(null)

const otherUsers = computed(() => users.value.filter((user) => user.id !== currentUser.value?.id))

const filterQuery = computed(() => ({
  searchQuery: searchQuery.value.trim() === "" ? undefined : searchQuery.value.trim(),
}))

async function fetchUsers() {
  if (searchQuery.value.trim() === "") {
    users.value = []
    totalCount.value = 0
    return
  }

  await userStore.fetchUsers(filterQuery.value, PAGE_SIZE, 0)
}

const infiniteScroll = useInfiniteScroll(
  window,
  async () => {
    await userStore.fetchUsers(filterQuery.value, PAGE_SIZE, users.value.length, {
      append: true,
    })
  },
  {
    distance: 200,
    canLoadMore: () => searchQuery.value.trim() !== "" && users.value.length < totalCount.value,
  },
)

watch(filterQuery, () => {
  fetchUsers()
  infiniteScroll.reset()
})

async function startChat(user: UserFieldsFragment) {
  startingChatWithUserId.value = user.id
  try {
    const chatId = await chatStore.startPrivateChat(user.id)
    router.push(`/chats/${chatId}`)
  } catch {
    notify.error("Не удалось открыть чат")
  } finally {
    startingChatWithUserId.value = null
  }
}
</script>

<template>
  <div class="flex animate-appear flex-col gap-6 p-6 sm:p-10">
    <h1 class="m-0 text-2xl font-semibold text-main">Пользователи</h1>

    <Input v-model="searchQuery" placeholder="Имя, фамилия, email..." />

    <div v-if="searchQuery.trim() === ''" class="px-5 py-8 text-center text-second">
      Начните вводить имя, фамилию или email, чтобы найти пользователя
    </div>

    <div v-else class="flex flex-col gap-2">
      <div
        v-for="user in otherUsers"
        :key="user.id"
        class="flex flex-col gap-4 rounded-card bg-card px-5 py-4 shadow-card sm:flex-row sm:items-center sm:justify-between"
      >
        <div class="flex min-w-0 flex-col gap-1.5">
          <span class="truncate text-[15px] font-medium text-main">{{ fullName(user) }}</span>
          <span class="truncate text-sm text-second">{{ user.email }}</span>
          <div class="flex flex-wrap gap-1.5">
            <Badge
              v-for="badge in userBadges(user)"
              :key="badge.label"
              :variant="badge.variant"
              :label="badge.label"
            />
          </div>
        </div>
        <div class="flex items-center gap-3">
          <Button
            icon="chats"
            :short-mode="false"
            class="w-full sm:w-auto"
            :disabled="startingChatWithUserId === user.id"
            @click="startChat(user)"
          >
            Написать
          </Button>
        </div>
      </div>

      <div v-if="otherUsers.length === 0" class="px-5 py-8 text-center text-second">
        Пользователи не найдены
      </div>

      <div v-if="infiniteScroll.isLoading.value" class="py-4 text-center text-second">
        Загрузка...
      </div>
    </div>
  </div>
</template>
