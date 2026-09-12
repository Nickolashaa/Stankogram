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
      class="glass-strong hairline shadow-float mx-4 flex w-full max-w-[400px] animate-rise flex-col gap-7 rounded-card px-6 py-10 sm:px-10 sm:py-12"
    >
      <AppBrand />
      <LoginForm v-model:email="loginEmail" />
      <PasswordResetForm :login-email="loginEmail" />
    </div>
  </main>
</template>
