<script setup lang="ts">
import { storeToRefs } from "pinia"
import { useAuthStore } from "@/stores/auth"
import { roleLabels } from "@/lib/roles"
import { fullName } from "@/lib/format"

const authStore = useAuthStore()
const { user } = storeToRefs(authStore)
</script>

<template>
  <div
    class="mx-auto flex h-full w-full max-w-2xl animate-appear flex-col justify-center gap-8 p-10"
  >
    <h1 class="m-0 text-3xl font-semibold text-main">Профиль</h1>

    <div v-if="user" class="flex flex-col gap-6 rounded-card bg-card p-10 shadow-card">
      <div class="flex flex-col gap-1">
        <span class="text-xs font-medium uppercase tracking-wide text-second">ID</span>
        <span class="text-lg text-main">{{ user.id }}</span>
      </div>
      <div class="flex flex-col gap-1">
        <span class="text-xs font-medium uppercase tracking-wide text-second">ФИО</span>
        <span class="text-lg text-main">{{ fullName(user) }}</span>
      </div>
      <div class="flex flex-col gap-1">
        <span class="text-xs font-medium uppercase tracking-wide text-second">Email</span>
        <span class="text-lg text-main">{{ user.email }}</span>
      </div>
      <div class="flex flex-col gap-1">
        <span class="text-xs font-medium uppercase tracking-wide text-second">Роль</span>
        <span class="text-lg text-main">{{ roleLabels[user.role] ?? user.role }}</span>
      </div>
      <div class="flex flex-col gap-1">
        <span class="text-xs font-medium uppercase tracking-wide text-second"
          >Права администратора</span
        >
        <span class="text-lg text-main">{{ user.isAdmin ? "Да" : "Нет" }}</span>
      </div>
    </div>
    <div v-else class="text-second">Загрузка...</div>
  </div>
</template>
