<script setup lang="ts">
import Input from "@/components/input.vue"
import Button from "@/components/button.vue"
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import { notify } from "@/lib/notify"

const router = useRouter()
const authStore = useAuthStore()

const email = defineModel<string>("email", { default: "" })
const password = ref("")

async function handleSubmit() {
  try {
    await authStore.login(email.value, password.value)
  } catch {
    notify.error("Неверный email или пароль")
    return
  }
  router.push("/")
}
</script>

<template>
  <form class="flex flex-col gap-4" @submit.prevent="handleSubmit">
    <Input placeholder="Email" v-model="email" />
    <Input placeholder="Пароль" type="password" v-model="password" />
    <Button type="submit">Войти</Button>
  </form>
</template>
