<script setup lang="ts">
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useAuthStore } from "@/stores/auth"
import { shortName, formatFullDate } from "@/lib/format"
import { getGreeting, getDayPeriod } from "@/lib/greeting"
import TimeOfDayIcon from "@/components/time-of-day-icon.vue"
import NavIcon, { type IconName } from "@/components/nav-icon.vue"

const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

const now = new Date()
const period = getDayPeriod(now.getHours())

const greeting = computed(() => (user.value ? getGreeting(shortName(user.value)) : ""))
const today = formatFullDate(now)

const shortcuts = computed(() => {
  const items: { to: string; label: string; description: string; icon: IconName }[] = [
    { to: "/users", label: "Написать", description: "Найти коллегу и начать личный чат", icon: "users" },
    { to: "/chats", label: "Чаты", description: "Личные и групповые обсуждения", icon: "chats" },
    { to: "/support", label: "Поддержка", description: "Задать вопрос команде", icon: "support" },
  ]

  if (user.value?.isAdmin) {
    items.push({
      to: "/admin",
      label: "Админка",
      description: "Управление системой",
      icon: "admin",
    })
  }

  return items
})
</script>

<template>
  <div
    class="flex h-full min-h-[60vh] flex-col items-center justify-center gap-8 p-6 sm:gap-10 sm:p-10"
  >
    <div class="flex animate-appear flex-col items-center gap-5 text-center">
      <div class="relative flex h-28 w-28 items-center justify-center">
        <div class="absolute inset-0 rounded-full bg-accent/10 blur-xl"></div>
        <div class="relative h-20 w-20">
          <TimeOfDayIcon :period="period" />
        </div>
      </div>

      <div class="flex flex-col gap-1.5">
        <h1 class="m-0 text-3xl font-semibold text-main">{{ greeting }}</h1>
        <span class="text-sm text-second">{{ today }}</span>
      </div>
    </div>

    <div class="grid w-full max-w-3xl grid-cols-1 gap-4 sm:grid-cols-2">
      <RouterLink
        v-for="(item, index) in shortcuts"
        :key="item.to"
        :to="item.to"
        class="group flex animate-appear items-center gap-4 rounded-card bg-card px-5 py-4 shadow-card transition-transform duration-200 hover:-translate-y-0.5"
        :style="{ animationDelay: `${index * 80}ms` }"
      >
        <span
          class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-accent/10 text-accent transition-colors duration-200 group-hover:bg-accent group-hover:text-bg"
        >
          <NavIcon :name="item.icon" />
        </span>
        <span class="flex min-w-0 flex-1 flex-col gap-0.5">
          <span class="text-[15px] font-medium text-main">{{ item.label }}</span>
          <span class="truncate text-xs text-second">{{ item.description }}</span>
        </span>
        <NavIcon
          name="arrow-right"
          :size="16"
          class="shrink-0 text-second opacity-0 transition-opacity duration-200 group-hover:opacity-100"
        />
      </RouterLink>
    </div>
  </div>
</template>
