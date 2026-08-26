<script setup lang="ts">
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import { roleLabels } from "@/lib/roles"
import { formatDateTime, fullName } from "@/lib/format"
import Button from "@/components/button.vue"
import Badge from "@/components/badge.vue"

defineProps<{
  users: UserFieldsFragment[]
}>()

defineEmits<{
  edit: [user: UserFieldsFragment]
  delete: [user: UserFieldsFragment]
}>()
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
          <td class="px-5 py-3 text-main">{{ fullName(user) }}</td>
          <td class="px-5 py-3 text-main">{{ user.email }}</td>
          <td class="px-5 py-3 text-main">
            <Badge variant="role">{{ roleLabels[user.role] }}</Badge>
          </td>
          <td class="px-5 py-3 text-main">{{ user.isAdmin ? "Да" : "Нет" }}</td>
          <td class="px-5 py-3 text-second">{{ formatDateTime(user.createdAt) }}</td>
          <td class="px-5 py-3 text-second">{{ formatDateTime(user.updatedAt) }}</td>
          <td class="px-5 py-3">
            <div class="flex justify-end gap-2">
              <Button
                variant="ghost"
                icon="edit"
                class="!text-accent hover:!text-accent-hover"
                aria-label="Редактировать"
                title="Редактировать"
                @click="$emit('edit', user)"
              >
                Редактировать
              </Button>
              <Button
                variant="ghost"
                icon="delete"
                class="!text-red-600 hover:!text-red-700"
                aria-label="Удалить"
                title="Удалить"
                @click="$emit('delete', user)"
              >
                Удалить
              </Button>
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
