<script setup lang="ts">
import { computed, ref } from "vue"
import { useRouter } from "vue-router"
import { storeToRefs } from "pinia"
import { useAuthStore } from "@/stores/auth"
import { shortName, initials } from "@/lib/format"
import { roleLabels } from "@/lib/roles"
import AppBrand from "@/components/app-brand.vue"
import NavIcon from "@/components/nav-icon.vue"
import Avatar from "@/components/avatar.vue"
import ThemePickerPanel from "@/components/theme-picker-panel.vue"

const router = useRouter()
const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

const themePickerOpen = ref(false)

const navItems = computed(() => {
  const items: {
    to: string
    label: string
    icon: "home" | "chats" | "users" | "support" | "admin"
  }[] = [
    { to: "/home", label: "Главная", icon: "home" },
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
    class="sticky top-0 flex h-screen w-64 shrink-0 flex-col justify-between overflow-y-auto border-r border-second/10 bg-card px-4 py-8"
  >
    <div class="flex flex-col gap-8">
      <div class="px-1">
        <AppBrand />
      </div>
      <div class="flex flex-col gap-1">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          v-slot="{ isActive, href, navigate }"
          :to="item.to"
          custom
        >
          <a
            :href="href"
            class="flex cursor-pointer items-center gap-3 rounded-input px-3 py-2.5 text-[15px] font-medium transition-colors duration-150"
            :class="isActive ? 'text-main' : 'text-second hover:bg-accent/5 hover:text-main'"
            @click="navigate"
          >
            <span
              class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full transition-colors duration-200"
              :class="isActive ? 'bg-accent text-bg' : 'bg-second/10 text-second'"
            >
              <NavIcon :name="item.icon" :size="18" />
            </span>
            {{ item.label }}
          </a>
        </RouterLink>
      </div>
    </div>

    <div class="flex flex-col gap-1">
      <div
        v-if="user"
        class="mb-2 flex items-center gap-3 rounded-input border-t border-second/10 px-3 pt-4"
      >
        <Avatar :label="initials(user)" size="sm" />
        <div class="flex min-w-0 flex-col">
          <span class="truncate text-sm font-medium text-main">{{ shortName(user) }}</span>
          <span class="truncate text-xs text-second">{{ roleLabels[user.role] }}</span>
        </div>
      </div>

      <button
        type="button"
        class="flex cursor-pointer items-center gap-3 rounded-input px-3 py-2.5 text-[15px] font-medium text-second transition-colors duration-150 hover:bg-accent/5 hover:text-main"
        @click="themePickerOpen = true"
      >
        <span
          class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-second/10 text-second"
        >
          <NavIcon name="palette" :size="18" />
        </span>
        Тема
      </button>
      <button
        type="button"
        class="flex cursor-pointer items-center gap-3 rounded-input px-3 py-2.5 text-[15px] font-medium text-second transition-colors duration-150 hover:bg-accent/5 hover:text-main"
        @click="handleLogout"
      >
        <span
          class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-second/10 text-second"
        >
          <NavIcon name="logout" :size="18" />
        </span>
        Выйти
      </button>
    </div>
  </nav>

  <ThemePickerPanel :open="themePickerOpen" @close="themePickerOpen = false" />
</template>
