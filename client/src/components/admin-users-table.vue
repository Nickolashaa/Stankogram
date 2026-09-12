<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import { roleLabels } from "@/lib/roles"
import { formatDateTime, fullName } from "@/lib/format"
import Badge from "@/components/badge.vue"

const props = defineProps<{
  users: UserFieldsFragment[]
}>()

const emit = defineEmits<{
  edit: [user: UserFieldsFragment]
  delete: [user: UserFieldsFragment]
}>()

type UserContextMenu = {
  x: number
  y: number
  user: UserFieldsFragment
}

const MENU_WIDTH = 208
const MENU_HEIGHT = 96

const contextMenu = ref<UserContextMenu | null>(null)

function closeContextMenu() {
  contextMenu.value = null
}

function openContextMenu(event: MouseEvent, user: UserFieldsFragment) {
  event.preventDefault()
  contextMenu.value = {
    x: Math.min(event.clientX, window.innerWidth - MENU_WIDTH - 8),
    y: Math.min(event.clientY, window.innerHeight - MENU_HEIGHT - 8),
    user,
  }
}

function handleEdit() {
  const user = contextMenu.value?.user
  closeContextMenu()
  if (user !== undefined) {
    emit("edit", user)
  }
}

function handleDelete() {
  const user = contextMenu.value?.user
  closeContextMenu()
  if (user !== undefined) {
    emit("delete", user)
  }
}

function handleEscape(event: KeyboardEvent) {
  if (event.key === "Escape") {
    closeContextMenu()
  }
}

onMounted(() => window.addEventListener("keydown", handleEscape))
onUnmounted(() => window.removeEventListener("keydown", handleEscape))
</script>

<template>
  <div class="glass hairline shadow-card overflow-x-auto rounded-card">
    <table class="w-full border-collapse text-left text-[15px]">
      <thead>
        <tr class="hairline-b text-xs font-semibold tracking-wider text-second uppercase">
          <th class="px-5 py-3 font-medium">ID</th>
          <th class="px-5 py-3 font-medium">ФИО</th>
          <th class="px-5 py-3 font-medium">Email</th>
          <th class="px-5 py-3 font-medium">Роль</th>
          <th class="px-5 py-3 font-medium">Админ</th>
          <th class="px-5 py-3 font-medium">Создан</th>
          <th class="px-5 py-3 font-medium">Обновлён</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="user in props.users"
          :key="user.id"
          class="hairline-b cursor-context-menu transition-colors duration-200 last:border-0 hover:bg-main/5"
          @contextmenu="openContextMenu($event, user)"
        >
          <td class="px-5 py-3 text-second">{{ user.id }}</td>
          <td class="px-5 py-3 text-main">{{ fullName(user) }}</td>
          <td class="px-5 py-3 text-main">{{ user.email }}</td>
          <td class="px-5 py-3 text-main">
            <Badge variant="role" :label="roleLabels[user.role]" />
          </td>
          <td class="px-5 py-3 text-main">{{ user.isAdmin ? "Да" : "Нет" }}</td>
          <td class="px-5 py-3 text-second">{{ formatDateTime(user.createdAt) }}</td>
          <td class="px-5 py-3 text-second">{{ formatDateTime(user.updatedAt) }}</td>
        </tr>
        <tr v-if="props.users.length === 0">
          <td colspan="7" class="px-5 py-8 text-center text-second">Пользователи не найдены</td>
        </tr>
      </tbody>
    </table>

    <div
      v-if="contextMenu"
      class="fixed inset-0 z-40"
      @click="closeContextMenu"
      @contextmenu.prevent="closeContextMenu"
    />

    <div
      v-if="contextMenu"
      class="glass-strong hairline shadow-float fixed z-50 flex w-56 origin-top-left animate-pop flex-col gap-0.5 overflow-hidden rounded-card p-1.5"
      :style="{ top: `${contextMenu.y}px`, left: `${contextMenu.x}px` }"
    >
      <span class="truncate px-3 pt-1.5 pb-2 text-xs font-semibold text-second">
        {{ fullName(contextMenu.user) }}
      </span>

      <button
        type="button"
        class="press cursor-pointer rounded-input px-3 py-2 text-left text-sm text-main hover:bg-main/6"
        @click="handleEdit"
      >
        Редактировать
      </button>

      <button
        type="button"
        class="press cursor-pointer rounded-input px-3 py-2 text-left text-sm text-red-600 hover:bg-red-500/12 dark:text-red-400"
        @click="handleDelete"
      >
        Удалить
      </button>
    </div>
  </div>
</template>
