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
    class="glass hairline-r sticky top-0 hidden h-dvh w-68 shrink-0 flex-col justify-between overflow-y-auto px-4 py-8 lg:flex"
  >
    <div class="flex flex-col gap-9">
      <div class="px-1">
        <AppBrand />
      </div>
      <div class="flex flex-col gap-1.5">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          v-slot="{ isActive, href, navigate }"
          :to="item.to"
          custom
        >
          <a
            :href="href"
            class="press group relative flex cursor-pointer items-center gap-3 overflow-hidden rounded-card px-2.5 py-2.5 text-[15px] font-medium"
            :class="isActive ? 'pill-active' : 'pill-idle'"
            @click="navigate"
          >
            <span
              class="flex h-9 w-9 shrink-0 items-center justify-center rounded-input transition-all duration-300"
              :class="
                isActive ? 'accent-surface glow-accent text-bg' : 'chip-idle group-hover:text-main'
              "
            >
              <NavIcon :name="item.icon" :size="18" />
            </span>
            {{ item.label }}
            <span
              v-if="item.unread"
              class="glow-accent ml-auto h-2 w-2 shrink-0 rounded-full bg-accent"
            />
          </a>
        </RouterLink>
      </div>
    </div>

    <div class="flex flex-col gap-1">
      <div
        v-if="user"
        class="mb-3 flex items-center gap-3 rounded-card bg-main/4 px-3 py-3 ring-1 ring-main/6 ring-inset"
      >
        <Avatar :label="initials(user)" size="sm" />
        <div class="flex min-w-0 flex-col">
          <span class="truncate text-sm font-medium text-main">{{ shortName(user) }}</span>
          <span class="truncate text-xs text-second">{{ roleLabels[user.role] }}</span>
        </div>
      </div>

      <RouterLink
        to="/support"
        class="press group flex cursor-pointer items-center gap-3 rounded-card px-2.5 py-2 text-[15px] font-medium text-second hover:bg-main/5 hover:text-main"
      >
        <span
          class="chip-idle flex h-9 w-9 shrink-0 items-center justify-center group-hover:text-main"
        >
          <NavIcon name="support" :size="18" />
        </span>
        Поддержка
      </RouterLink>
      <button
        type="button"
        class="press group flex cursor-pointer items-center gap-3 rounded-card px-2.5 py-2 text-[15px] font-medium text-second hover:bg-main/5 hover:text-main"
        @click="themePickerOpen = true"
      >
        <span
          class="chip-idle flex h-9 w-9 shrink-0 items-center justify-center group-hover:text-main"
        >
          <NavIcon name="palette" :size="18" />
        </span>
        Тема
      </button>
      <button
        type="button"
        class="press group flex cursor-pointer items-center gap-3 rounded-card px-2.5 py-2 text-[15px] font-medium text-second hover:bg-red-500/8 hover:text-red-600 dark:hover:text-red-400"
        @click="handleLogout"
      >
        <span
          class="chip-idle flex h-9 w-9 shrink-0 items-center justify-center group-hover:bg-red-500/12 group-hover:text-red-600 dark:group-hover:text-red-400"
        >
          <NavIcon name="logout" :size="18" />
        </span>
        Выйти
      </button>
    </div>
  </nav>

  <nav
    v-if="!hideMobileNav"
    class="mobile-bar glass hairline shadow-float z-40 flex h-16 items-center justify-around px-2 lg:hidden"
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
        class="press flex flex-1 cursor-pointer flex-col items-center gap-1 rounded-input px-2 py-1.5 text-[10px] font-medium"
        :class="isActive ? 'text-main' : 'text-second'"
        @click="navigate"
      >
        <span
          class="relative flex h-9 w-9 shrink-0 items-center justify-center rounded-input transition-all duration-300"
          :class="isActive ? 'accent-surface glow-accent text-bg' : 'text-second'"
        >
          <NavIcon :name="item.icon" :size="18" />
          <span
            v-if="item.unread"
            class="absolute -top-0.5 -right-0.5 h-2 w-2 rounded-full bg-accent ring-2 ring-card"
          />
        </span>
        {{ item.label }}
      </a>
    </RouterLink>

    <button
      type="button"
      class="press flex flex-1 cursor-pointer flex-col items-center justify-center rounded-input px-2 py-1.5"
      aria-label="Профиль"
      @click="mobileMenuOpen = true"
    >
      <Avatar v-if="user" :label="initials(user)" size="sm" />
    </button>
  </nav>

  <div
    v-if="mobileMenuOpen"
    class="fixed inset-0 z-50 flex animate-appear items-end bg-black/45 backdrop-blur-sm lg:hidden"
    @click.self="mobileMenuOpen = false"
  >
    <div
      class="glass-strong hairline shadow-float flex w-full animate-slide-up flex-col gap-1 rounded-t-card px-4 pt-3 pb-[calc(1rem+env(safe-area-inset-bottom))]"
    >
      <span class="mx-auto mb-3 h-1 w-10 shrink-0 rounded-full bg-main/15" />

      <div v-if="user" class="hairline-b mb-2 flex items-center gap-3 px-2 pb-4">
        <Avatar :label="initials(user)" size="md" />
        <div class="flex min-w-0 flex-col">
          <span class="truncate text-sm font-medium text-main">{{ shortName(user) }}</span>
          <span class="truncate text-xs text-second">{{ roleLabels[user.role] }}</span>
        </div>
      </div>

      <RouterLink
        to="/support"
        class="press group flex cursor-pointer items-center gap-3 rounded-card px-2.5 py-2.5 text-[15px] font-medium text-second hover:bg-main/5 hover:text-main"
        @click="mobileMenuOpen = false"
      >
        <span
          class="chip-idle flex h-9 w-9 shrink-0 items-center justify-center group-hover:text-main"
        >
          <NavIcon name="support" :size="18" />
        </span>
        Поддержка
      </RouterLink>
      <button
        type="button"
        class="press group flex cursor-pointer items-center gap-3 rounded-card px-2.5 py-2.5 text-[15px] font-medium text-second hover:bg-main/5 hover:text-main"
        @click="openThemePicker"
      >
        <span
          class="chip-idle flex h-9 w-9 shrink-0 items-center justify-center group-hover:text-main"
        >
          <NavIcon name="palette" :size="18" />
        </span>
        Тема
      </button>
      <button
        type="button"
        class="press group flex cursor-pointer items-center gap-3 rounded-card px-2.5 py-2.5 text-[15px] font-medium text-second hover:bg-red-500/8 hover:text-red-600 dark:hover:text-red-400"
        @click="handleLogout"
      >
        <span
          class="chip-idle flex h-9 w-9 shrink-0 items-center justify-center group-hover:bg-red-500/12 group-hover:text-red-600 dark:group-hover:text-red-400"
        >
          <NavIcon name="logout" :size="18" />
        </span>
        Выйти
      </button>
      <button
        type="button"
        class="press mt-1 cursor-pointer rounded-card bg-main/5 px-3 py-2.5 text-center text-[15px] font-medium text-second hover:text-main"
        @click="mobileMenuOpen = false"
      >
        Закрыть
      </button>
    </div>
  </div>

  <ThemePickerPanel :open="themePickerOpen" @close="themePickerOpen = false" />
</template>
