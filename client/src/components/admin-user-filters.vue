<script setup lang="ts">
import Input from "@/components/input.vue"
import Select from "@/components/select.vue"
import type { components } from "@/api/schema"

type Role = components["schemas"]["Role"]

const search = defineModel<string>("search", { default: "" })
const role = defineModel<"" | Role>("role", { default: "" })
const isAdmin = defineModel<"" | "true" | "false">("isAdmin", { default: "" })
</script>

<template>
  <div class="flex flex-wrap items-end gap-3">
    <div class="flex min-w-[240px] flex-1 flex-col gap-1">
      <label class="text-xs font-medium uppercase tracking-wide text-second">Поиск</label>
      <Input v-model="search" placeholder="Имя, фамилия, email..." />
    </div>
    <div class="flex w-48 flex-col gap-1">
      <label class="text-xs font-medium uppercase tracking-wide text-second">Роль</label>
      <Select v-model="role">
        <option value="">Все роли</option>
        <option value="STUDENT">Студент</option>
        <option value="TEACHER">Преподаватель</option>
      </Select>
    </div>
    <div class="flex w-48 flex-col gap-1">
      <label class="text-xs font-medium uppercase tracking-wide text-second">Админ</label>
      <Select v-model="isAdmin">
        <option value="">Все</option>
        <option value="true">Да</option>
        <option value="false">Нет</option>
      </Select>
    </div>
  </div>
</template>
