<script setup lang="ts">
import Input from "@/components/input.vue"
import Button from "@/components/button.vue"
import { ref } from "vue"
import { useAuthStore } from "@/stores/auth"
import { notify } from "@/lib/notify"

const props = defineProps<{
  loginEmail?: string
}>()

const authStore = useAuthStore()

const showForm = ref(false)
const email = ref("")
const loading = ref(false)

function openForm() {
  if (props.loginEmail) {
    email.value = props.loginEmail
  }
  showForm.value = true
}

async function handleSubmit() {
  loading.value = true

  try {
    await authStore.requestPasswordReset(email.value)
  } catch {
    notify.error("Не удалось отправить письмо. Проверьте email и попробуйте ещё раз")
    return
  } finally {
    loading.value = false
  }

  notify.success(
    "Мы отправили ссылку для сброса пароля на почту. Проверьте входящие и обязательно загляните в папку «Спам»",
  )
  showForm.value = false
  email.value = ""
}
</script>

<template>
  <Button v-if="!showForm" variant="ghost" @click="openForm">Забыли пароль?</Button>

  <form v-else class="flex animate-appear flex-col gap-3" @submit.prevent="handleSubmit">
    <p class="m-0 text-sm text-second">Введите email — пришлём ссылку для сброса пароля</p>
    <Input placeholder="Email" type="email" v-model="email" />
    <div class="flex gap-2">
      <Button type="button" variant="ghost" class="flex-1" @click="showForm = false">
        Отмена
      </Button>
      <Button type="submit" class="flex-[2]" :disabled="loading">Отправить</Button>
    </div>
  </form>
</template>
