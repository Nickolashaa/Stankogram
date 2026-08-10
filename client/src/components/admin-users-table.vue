<script setup lang="ts">
import type { components } from "@/api/schema"
import { roleLabels } from "@/lib/roles"

type UserResponse = components["schemas"]["UserResponse"]

defineProps<{
  users: UserResponse[]
}>()

defineEmits<{
  edit: [user: UserResponse]
  delete: [user: UserResponse]
}>()

function formatDate(value: string) {
  return new Date(value).toLocaleString("ru-RU", {
    dateStyle: "short",
    timeStyle: "short",
  })
}
</script>

<template>
  <div class="overflow-x-auto rounded-card bg-card shadow-card">
    <table class="w-full border-collapse text-left text-[15px]">
      <thead>
        <tr
          class="border-b border-second/15 text-xs font-medium uppercase tracking-wide text-second"
        >
          <th class="px-5 py-3 font-medium">ID</th>
          <th class="px-5 py-3 font-medium">ФИО</th>
          <th class="px-5 py-3 font-medium">Email</th>
          <th class="px-5 py-3 font-medium">Роль</th>
          <th class="px-5 py-3 font-medium">Админ</th>
          <th class="px-5 py-3 font-medium">Создан</th>
          <th class="px-5 py-3 font-medium">Обновлён</th>
          <th class="px-5 py-3 font-medium"></th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="user in users"
          :key="user.id"
          class="border-b border-second/10 last:border-0 hover:bg-accent/5"
        >
          <td class="px-5 py-3 text-second">{{ user.id }}</td>
          <td class="px-5 py-3 text-main">
            {{ [user.surname, user.name, user.patronymic].filter(Boolean).join(" ") }}
          </td>
          <td class="px-5 py-3 text-main">{{ user.email }}</td>
          <td class="px-5 py-3 text-main">{{ roleLabels[user.role] }}</td>
          <td class="px-5 py-3 text-main">{{ user.is_admin ? "Да" : "Нет" }}</td>
          <td class="px-5 py-3 text-second">{{ formatDate(user.created_at) }}</td>
          <td class="px-5 py-3 text-second">{{ formatDate(user.updated_at) }}</td>
          <td class="px-5 py-3">
            <div class="flex justify-end gap-4">
              <button
                type="button"
                class="cursor-pointer text-sm font-medium text-accent transition-colors duration-150 hover:text-accent-hover"
                @click="$emit('edit', user)"
              >
                Редактировать
              </button>
              <button
                type="button"
                class="cursor-pointer text-sm font-medium text-red-600 transition-colors duration-150 hover:text-red-700"
                @click="$emit('delete', user)"
              >
                Удалить
              </button>
            </div>
          </td>
        </tr>
        <tr v-if="users.length === 0">
          <td colspan="8" class="px-5 py-8 text-center text-second">Пользователи не найдены</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
