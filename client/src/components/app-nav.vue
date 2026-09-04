<script setup lang="ts">
import { computed, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { storeToRefs } from "pinia"
import { useAuthStore } from "@/stores/auth"
import { useChatStore } from "@/stores/chats"
import { shortName, initials } from "@/lib/format"
import { roleLabels } from "@/lib/roles"
import AppBrand from "@/components/app-brand.vue"
import NavIcon from "@/components/nav-icon.vue"
import Avatar from "@/components/avatar.vue"
import ThemePickerPanel from "@/components/theme-picker-panel.vue"

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()
const { user } = storeToRefs(authStore)
const { hasUnread } = storeToRefs(chatStore)

const themePickerOpen = ref(false)
const mobileMenuOpen = ref(false)

const hideMobileNav = computed(() => /^\/chats\/\d+/.test(route.path))

const navItems = computed(() => {
  const items: {
    to: string
    label: string
    icon: "home" | "chats" | "users" | "support" | "admin"
    unread?: boolean
  }[] = [
    { to: "/home", label: "Главная", icon: "home" },
    { to: "/chats", label: "Чаты", icon: "chats", unread: hasUnread.value },
  ]

  if (user.value?.isAdmin) {
    items.push({ to: "/admin", label: "Админка", icon: "admin" })
  }

  return items
})

async function handleLogout() {
  mobileMenuOpen.value = false
  await authStore.logout()
  router.push("/auth")
}

function openThemePicker() {
  mobileMenuOpen.value = false
  themePickerOpen.value = true
}
</script>

<template>
  <nav
    class="sticky top-0 hidden h-dvh w-64 shrink-0 flex-col justify-between overflow-y-auto border-r border-second/10 bg-card px-4 py-8 lg:flex"
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
            <span v-if="item.unread" class="h-2 w-2 shrink-0 rounded-full bg-accent" />
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

      <RouterLink
        to="/support"
        class="flex cursor-pointer items-center gap-3 rounded-input px-3 py-2.5 text-[15px] font-medium text-second transition-colors duration-150 hover:bg-accent/5 hover:text-main"
      >
        <span
          class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-second/10 text-second"
        >
          <NavIcon name="support" :size="18" />
        </span>
        Поддержка
      </RouterLink>
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

  <nav
    v-if="!hideMobileNav"
    class="fixed inset-x-0 bottom-0 z-40 flex h-16 items-center justify-around border-t border-second/10 bg-card px-1 pb-[env(safe-area-inset-bottom)] lg:hidden"
  >
    <RouterLink
      v-for="item in navItems"
      :key="item.to"
      v-slot="{ isActive, href, navigate }"
      :to="item.to"
      custom
    >
      <a
        :href="href"
        class="flex cursor-pointer flex-col items-center gap-1 rounded-input px-2 py-1.5 text-[10px] font-medium"
        :class="isActive ? 'text-main' : 'text-second'"
        @click="navigate"
      >
        <span
          class="relative flex h-8 w-8 shrink-0 items-center justify-center rounded-full transition-colors duration-200"
          :class="isActive ? 'bg-accent text-bg' : 'text-second'"
        >
          <NavIcon :name="item.icon" :size="18" />
          <span
            v-if="item.unread"
            class="absolute top-0 right-0 h-2 w-2 rounded-full bg-accent ring-2 ring-card"
          />
        </span>
        {{ item.label }}
      </a>
    </RouterLink>

    <button
      type="button"
      class="flex cursor-pointer flex-col items-center gap-1 rounded-input px-2 py-1.5 text-[10px] font-medium text-second"
      aria-label="Профиль"
      @click="mobileMenuOpen = true"
    >
      <Avatar v-if="user" :label="initials(user)" size="sm" />
    </button>
  </nav>

  <div
    v-if="mobileMenuOpen"
    class="fixed inset-0 z-50 flex animate-appear items-end bg-black/40 lg:hidden"
    @click.self="mobileMenuOpen = false"
  >
    <div
      class="flex w-full flex-col gap-1 rounded-t-card bg-card px-4 pt-4 pb-[calc(1rem+env(safe-area-inset-bottom))] shadow-card"
    >
      <div v-if="user" class="mb-2 flex items-center gap-3 border-b border-second/10 px-2 pb-4">
        <Avatar :label="initials(user)" size="sm" />
        <div class="flex min-w-0 flex-col">
          <span class="truncate text-sm font-medium text-main">{{ shortName(user) }}</span>
          <span class="truncate text-xs text-second">{{ roleLabels[user.role] }}</span>
        </div>
      </div>

      <RouterLink
        to="/support"
        class="flex cursor-pointer items-center gap-3 rounded-input px-3 py-2.5 text-[15px] font-medium text-second transition-colors duration-150 hover:bg-accent/5 hover:text-main"
        @click="mobileMenuOpen = false"
      >
        <span
          class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-second/10 text-second"
        >
          <NavIcon name="support" :size="18" />
        </span>
        Поддержка
      </RouterLink>
      <button
        type="button"
        class="flex cursor-pointer items-center gap-3 rounded-input px-3 py-2.5 text-[15px] font-medium text-second transition-colors duration-150 hover:bg-accent/5 hover:text-main"
        @click="openThemePicker"
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
      <button
        type="button"
        class="cursor-pointer rounded-input px-3 py-2.5 text-left text-[15px] font-medium text-second transition-colors duration-150 hover:bg-accent/5 hover:text-main"
        @click="mobileMenuOpen = false"
      >
        Закрыть
      </button>
    </div>
  </div>

  <ThemePickerPanel :open="themePickerOpen" @close="themePickerOpen = false" />
</template>
