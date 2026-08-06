<script setup lang="ts">
import Input from '@/components/input.vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const authForm = ref<{
  login: string,
  password: string,
}>({
  login: '',
  password: '',
});

async function handleSubmit() {
  await authStore.login(authForm.value.login, authForm.value.password);
  router.push('/');
}
</script>

<template>
  <main>
    <div class="flex w-full max-w-[380px] animate-appear flex-col gap-6 rounded-card bg-card px-10 py-12 shadow-card">
      <div class="flex flex-col gap-1.5 text-center">
        <h1 class="m-0 text-2xl font-semibold text-main">Stankogram</h1>
        <h2 class="m-0 text-sm font-normal text-second">Университетский мессенджер</h2>
      </div>

      <form class="flex flex-col gap-4" @submit.prevent="handleSubmit">
        <Input placeholder="Логин" v-model="authForm.login"/>
        <Input placeholder="Пароль" type="password" v-model="authForm.password"/>
        <button
          type="submit"
          class="h-12 cursor-pointer rounded-input bg-accent text-[15px] font-semibold text-bg transition-colors duration-150 hover:bg-accent-hover"
        >Войти</button>
      </form>
    </div>
  </main>
</template>
