<script setup lang="ts">
import { computed } from "vue"
import { useRouter } from "vue-router"
import { storeToRefs } from "pinia"
import { useAuthStore } from "@/stores/auth"
import AppBrand from "@/components/app-brand.vue"
import Button from "@/components/button.vue"

const router = useRouter()
const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

const navItems = computed(() => {
  const items = [
    { to: "/chats", label: "Чаты" },
    { to: "/users", label: "Пользователи" },
    { to: "/profile", label: "Профиль" },
    { to: "/support", label: "Поддержка" },
  ]

  if (user.value?.is_admin) {
    items.push({ to: "/admin", label: "Админка" })
  }

  return items
})

async function handleLogout() {
  await authStore.logout()
  router.push("/auth")
}
</script>

<template>
  <nav
    class="flex w-64 shrink-0 flex-col justify-between border-r border-second/15 bg-card px-5 py-8"
  >
    <div class="flex flex-col gap-8">
      <AppBrand />
      <div class="flex flex-col gap-1">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="rounded-input px-4 py-2.5 text-[15px] font-medium text-second transition-colors duration-150 hover:bg-accent/10 hover:text-main"
          active-class="bg-accent/10 text-accent"
        >
          {{ item.label }}
        </RouterLink>
      </div>
    </div>
    <div class="flex flex-col gap-3">
      <Button variant="ghost" @click="handleLogout">Выйти</Button>
    </div>
  </nav>
</template>
