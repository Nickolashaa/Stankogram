<script setup lang="ts">
import AppBrand from "@/components/app-brand.vue"
import Button from "@/components/button.vue"
import { onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const status = ref<"loading" | "success" | "error">("loading")

onMounted(async () => {
  const id = Number(route.query.id)
  const code = String(route.query.code ?? "")

  if (!id || !code) {
    status.value = "error"
    return
  }

  try {
    await authStore.confirmPasswordReset(id, code)
    status.value = "success"
  } catch {
    status.value = "error"
  }
})
</script>

<template>
  <main>
    <div
      class="flex w-full max-w-[380px] animate-appear flex-col gap-6 rounded-card bg-card px-10 py-12 shadow-card text-center"
    >
      <AppBrand />

      <p v-if="status === 'loading'" class="m-0 text-sm text-second">Подтверждаем сброс пароля…</p>

      <p v-else-if="status === 'success'" class="m-0 text-sm text-second">
        Пароль сброшен. Новые данные для входа отправлены на почту.
      </p>

      <p v-else class="m-0 text-sm text-second">
        Ссылка недействительна или срок её действия истёк. Запросите сброс пароля ещё раз.
      </p>

      <Button
        v-if="status !== 'loading'"
        icon="arrow-right"
        :short-mode="false"
        @click="router.push('/auth')"
      >
        На страницу входа
      </Button>
    </div>
  </main>
</template>
