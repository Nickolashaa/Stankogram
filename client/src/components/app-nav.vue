<script setup lang="ts">
import { computed, ref } from "vue"
import { useRouter } from "vue-router"
import { storeToRefs } from "pinia"
import { useAuthStore } from "@/stores/auth"
import AppBrand from "@/components/app-brand.vue"
import NavIcon from "@/components/nav-icon.vue"
import ThemePickerPanel from "@/components/theme-picker-panel.vue"

const router = useRouter()
const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

const themePickerOpen = ref(false)

const navItems = computed(() => {
  const items: {
    to: string
    label: string
    icon: "chats" | "users" | "support" | "admin"
  }[] = [
    { to: "/chats", label: "Чаты", icon: "chats" },
    { to: "/users", label: "Пользователи", icon: "users" },
    { to: "/support", label: "Поддержка", icon: "support" },
  ]

  if (user.value?.isAdmin) {
    items.push({ to: "/admin", label: "Админка", icon: "admin" })
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
          class="flex items-center gap-3 rounded-input px-4 py-2.5 text-lg font-medium text-second transition-colors duration-150 hover:bg-accent/10 hover:text-main"
          active-class="bg-accent/10 text-accent"
        >
          <NavIcon :name="item.icon" />
          {{ item.label }}
        </RouterLink>
      </div>
    </div>
    <div class="flex flex-col gap-3">
      <button
        type="button"
        class="flex cursor-pointer items-center gap-3 rounded-input px-4 py-2.5 text-lg font-medium text-second transition-colors duration-150 hover:bg-accent/10 hover:text-accent"
        @click="themePickerOpen = true"
      >
        <NavIcon name="palette" />
        Тема
      </button>
      <button
        type="button"
        class="flex cursor-pointer items-center gap-3 rounded-input px-4 py-2.5 text-lg font-medium text-second transition-colors duration-150 hover:bg-accent/10 hover:text-accent"
        @click="handleLogout"
      >
        <NavIcon name="logout" />
        Выйти
      </button>
    </div>
  </nav>

  <ThemePickerPanel :open="themePickerOpen" @close="themePickerOpen = false" />
</template>
