<script setup lang="ts">
import { ref, watch } from "vue"
import Input from "@/components/input.vue"
import Select from "@/components/select.vue"
import Button from "@/components/button.vue"
import type { components } from "@/api/schema"

type UserInput = components["schemas"]["UserInput"]
type UserResponse = components["schemas"]["UserResponse"]
type Role = components["schemas"]["Role"]

const props = defineProps<{
  open: boolean
  title: string
  initialUser?: UserResponse | null
  submitting?: boolean
}>()

const emit = defineEmits<{
  close: []
  submit: [data: UserInput]
}>()

const name = ref("")
const surname = ref("")
const patronymic = ref("")
const email = ref("")
const role = ref<Role>("STUDENT")
const isAdmin = ref(false)

watch(
  () => props.open,
  (isOpen) => {
    if (!isOpen) {
      return
    }
    name.value = props.initialUser?.name ?? ""
    surname.value = props.initialUser?.surname ?? ""
    patronymic.value = props.initialUser?.patronymic ?? ""
    email.value = props.initialUser?.email ?? ""
    role.value = props.initialUser?.role ?? "STUDENT"
    isAdmin.value = props.initialUser?.is_admin ?? false
  },
  { immediate: true },
)

function handleClose() {
  emit("close")
}

function handleSubmit() {
  emit("submit", {
    name: name.value,
    surname: surname.value,
    patronymic: patronymic.value.trim() === "" ? null : patronymic.value,
    email: email.value,
    role: role.value,
    is_admin: isAdmin.value,
  })
}
</script>

<template>
  <div
    v-if="open"
    class="fixed inset-0 z-50 flex animate-appear items-center justify-center bg-black/40 px-4"
    @click.self="handleClose"
  >
    <form
      class="flex w-full max-w-md flex-col gap-4 rounded-card bg-card p-8 shadow-card"
      @submit.prevent="handleSubmit"
    >
      <h2 class="m-0 text-xl font-semibold text-main">{{ title }}</h2>

      <Input placeholder="Имя" v-model="name" />
      <Input placeholder="Фамилия" v-model="surname" />
      <Input placeholder="Отчество" v-model="patronymic" />
      <Input placeholder="Email" type="email" v-model="email" />

      <Select v-model="role">
        <option value="STUDENT">Студент</option>
        <option value="TEACHER">Преподаватель</option>
      </Select>

      <label class="flex items-center gap-2 text-[15px] text-main">
        <input type="checkbox" v-model="isAdmin" class="h-4 w-4 accent-accent" />
        Права администратора
      </label>

      <div class="mt-2 flex gap-2">
        <Button type="button" variant="ghost" class="flex-1" @click="handleClose">Отмена</Button>
        <Button type="submit" class="flex-[2]" :disabled="submitting">Сохранить</Button>
      </div>
    </form>
  </div>
</template>
