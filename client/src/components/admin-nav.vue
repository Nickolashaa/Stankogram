<script setup lang="ts">
import NavIcon from "@/components/nav-icon.vue"

const navItems: { to: string; label: string; icon: "users" | "chats" | "bell" }[] = [
  { to: "/admin/users", label: "Пользователи", icon: "users" },
  { to: "/admin/chats", label: "Групповые чаты", icon: "chats" },
  { to: "/admin/notifications", label: "Системные уведомления", icon: "bell" },
]
</script>

<template>
  <nav
    class="glass hairline-b flex shrink-0 gap-1.5 overflow-x-auto px-3 py-3 lg:w-72 lg:flex-col lg:overflow-visible lg:border-b-0 lg:py-8 lg:hairline-r"
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
        class="press group flex shrink-0 cursor-pointer items-center gap-3 rounded-card px-2.5 py-2.5 text-[15px] font-medium"
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
        <span class="whitespace-nowrap lg:whitespace-normal">{{ item.label }}</span>
      </a>
    </RouterLink>
  </nav>
</template>
