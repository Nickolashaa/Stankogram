<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import { storeToRefs } from "pinia"
import { useAuthStore } from "@/stores/auth"
import { useChatStore } from "@/stores/chats"
import { useSystemNotificationStore } from "@/stores/system-notifications"
import { shortName, formatFullDate, formatDateTime } from "@/lib/format"
import { getGreeting, getDayPeriod } from "@/lib/greeting"
import { notify } from "@/lib/notify"
import TimeOfDayIcon from "@/components/time-of-day-icon.vue"
import NavIcon, { type IconName } from "@/components/nav-icon.vue"
import Button from "@/components/button.vue"

const NOTIFICATIONS_PAGE_SIZE = 20

const authStore = useAuthStore()
const chatStore = useChatStore()
const notificationStore = useSystemNotificationStore()
const { user } = storeToRefs(authStore)
const { hasUnread } = storeToRefs(chatStore)
const { unreadNotifications } = storeToRefs(notificationStore)

onMounted(() => {
  notificationStore.fetchUnreadNotifications(NOTIFICATIONS_PAGE_SIZE, 0)
})

async function markNotificationRead(id: number) {
  try {
    await notificationStore.markNotificationRead(id)
  } catch {
    notify.error("Не удалось скрыть уведомление")
  }
}

const now = new Date()
const period = getDayPeriod(now.getHours())

const greeting = computed(() => (user.value ? getGreeting(shortName(user.value)) : ""))
const today = formatFullDate(now)

const shortcuts = computed(() => {
  const items: {
    to: string
    label: string
    description: string
    icon: IconName
    unread?: boolean
  }[] = [
    {
      to: "/users",
      label: "Написать",
      description: "Найти коллегу и начать личный чат",
      icon: "users",
    },
    {
      to: "/chats",
      label: "Чаты",
      description: "Личные и групповые обсуждения",
      icon: "chats",
      unread: hasUnread.value,
    },
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

const sunIcon = ref<InstanceType<typeof TimeOfDayIcon> | null>(null)
const isSunLaunched = computed(() => sunIcon.value?.launched ?? false)

function handleSunClick() {
  sunIcon.value?.boost()
}
</script>

<template>
  <div
    class="flex h-full min-h-[60vh] flex-col items-center justify-center gap-8 p-6 sm:gap-10 sm:p-10"
  >
    <div class="flex animate-appear flex-col items-center gap-5 text-center">
      <div class="relative flex h-28 w-28 items-center justify-center" @click="handleSunClick">
        <div
          class="absolute inset-0 rounded-full bg-accent/10 blur-xl transition-opacity duration-500"
          :class="isSunLaunched ? 'opacity-0' : 'opacity-100'"
        ></div>
        <div class="relative h-20 w-20">
          <TimeOfDayIcon ref="sunIcon" :period="period" />
          <svg
            v-if="isSunLaunched"
            viewBox="0 0 100 100"
            class="absolute inset-0 h-full w-full animate-sad-face-in text-accent"
          >
            <circle cx="50" cy="50" r="34" fill="none" stroke="currentColor" stroke-width="4" />
            <circle cx="38" cy="42" r="4" fill="currentColor" />
            <circle cx="62" cy="42" r="4" fill="currentColor" />
            <path
              d="M35 68 Q50 56 65 68"
              fill="none"
              stroke="currentColor"
              stroke-width="4"
              stroke-linecap="round"
            />
          </svg>
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
          <span class="flex items-center gap-2 text-[15px] font-medium text-main">
            {{ item.label }}
            <span v-if="item.unread" class="h-2 w-2 shrink-0 rounded-full bg-accent" />
          </span>
          <span class="truncate text-xs text-second">{{ item.description }}</span>
        </span>
        <NavIcon
          name="arrow-right"
          :size="16"
          class="shrink-0 text-second opacity-0 transition-opacity duration-200 group-hover:opacity-100"
        />
      </RouterLink>
    </div>

    <div
      v-if="unreadNotifications.length > 0"
      class="flex w-full max-w-3xl animate-appear flex-col gap-3"
    >
      <div class="flex items-center gap-2 text-second">
        <NavIcon name="bell" :size="16" />
        <span class="text-sm font-medium">Уведомления</span>
        <span class="h-2 w-2 shrink-0 rounded-full bg-accent" />
      </div>

      <div
        v-for="notification in unreadNotifications"
        :key="notification.id"
        class="flex items-start gap-4 rounded-card border-l-[3px] border-accent bg-card px-5 py-4 shadow-card"
      >
        <span class="flex min-w-0 flex-1 flex-col gap-1">
          <span class="text-[15px] whitespace-pre-wrap text-main">{{ notification.text }}</span>
          <span class="text-xs text-second">{{ formatDateTime(notification.createdAt) }}</span>
        </span>
        <Button
          icon="cancel"
          variant="ghost"
          title="Скрыть"
          aria-label="Скрыть"
          @click="markNotificationRead(notification.id)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-sad-face-in {
  opacity: 0;
  animation: sad-face-in 0.4s ease-out 0.7s forwards;
}

@keyframes sad-face-in {
  from {
    opacity: 0;
    transform: scale(0.7);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .animate-sad-face-in {
    animation: none;
    opacity: 1;
  }
}
</style>
