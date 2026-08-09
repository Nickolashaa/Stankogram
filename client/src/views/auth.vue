<script setup lang="ts">
import AppBrand from "@/components/app-brand.vue"
import LoginForm from "@/components/login-form.vue"
import PasswordResetForm from "@/components/password-reset-form.vue"
import { ref } from "vue"

const loginEmail = ref("")
</script>

<template>
  <main>
    <div
      class="flex w-full max-w-[380px] animate-appear flex-col gap-6 rounded-card bg-card px-10 py-12 shadow-card"
    >
      <AppBrand />
      <LoginForm v-model:email="loginEmail" />
      <PasswordResetForm :login-email="loginEmail" />
    </div>
  </main>
</template>
