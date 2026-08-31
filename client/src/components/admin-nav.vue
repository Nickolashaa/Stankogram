<script setup lang="ts">
import NavIcon from "@/components/nav-icon.vue"

const navItems: { to: string; label: string; icon: "users" | "chats" | "bell" }[] = [
  { to: "/admin/users", label: "Пользователи", icon: "users" },
  { to: "/admin/chats", label: "Групповые чаты", icon: "chats" },
  { to: "/admin/notifications", label: "Уведомления", icon: "bell" },
]
</script>

<template>
  <nav
    class="flex shrink-0 gap-1 overflow-x-auto border-b border-second/10 bg-card px-3 py-3 lg:w-56 lg:flex-col lg:overflow-visible lg:border-r lg:border-b-0 lg:py-8"
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
        class="flex shrink-0 cursor-pointer items-center gap-3 rounded-input px-3 py-2.5 text-[15px] font-medium transition-colors duration-150"
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
  </nav>
</template>
