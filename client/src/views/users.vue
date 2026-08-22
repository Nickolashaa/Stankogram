<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import { useUserStore } from "@/stores/users"
import { useAuthStore } from "@/stores/auth"
import { roleLabels } from "@/lib/roles"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import Input from "@/components/input.vue"

const userStore = useUserStore()
const authStore = useAuthStore()
const { users } = storeToRefs(userStore)
const { user: currentUser } = storeToRefs(authStore)

const searchQuery = ref("")

const otherUsers = computed(() => users.value.filter((user) => user.id !== currentUser.value?.id))

async function fetchUsers() {
  await userStore.fetchUsers(
    { searchQuery: searchQuery.value.trim() === "" ? undefined : searchQuery.value.trim() },
    50,
    0,
  )
}

watch(searchQuery, fetchUsers)

onMounted(fetchUsers)

function fullName(user: UserFieldsFragment) {
  return [user.surname, user.name, user.patronymic].filter(Boolean).join(" ")
}
</script>

<template>
  <div class="flex animate-appear flex-col gap-6 p-10">
    <h1 class="m-0 text-2xl font-semibold text-main">Пользователи</h1>

    <Input v-model="searchQuery" placeholder="Имя, фамилия, email..." />

    <div class="flex flex-col gap-2">
      <div
        v-for="user in otherUsers"
        :key="user.id"
        class="flex items-center justify-between gap-4 rounded-card bg-card px-5 py-4 shadow-card"
      >
        <div class="flex flex-col gap-1">
          <span class="text-[15px] font-medium text-main">{{ fullName(user) }}</span>
          <span class="text-sm text-second">{{ user.email }}</span>
        </div>
        <span class="text-sm text-second">{{ roleLabels[user.role] }}</span>
      </div>

      <div v-if="otherUsers.length === 0" class="px-5 py-8 text-center text-second">
        Пользователи не найдены
      </div>
    </div>
  </div>
</template>
