<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { storeToRefs } from "pinia"
import { useAuthStore } from "@/stores/auth"
import { useSystemNotificationStore } from "@/stores/system-notifications"
import { useNotificationStore } from "@/stores/notifications"
import { shortName, formatFullDate, formatDateTime } from "@/lib/format"
import { getGreeting, getDayPeriod } from "@/lib/greeting"
import { notify } from "@/lib/notify"
import TimeOfDayIcon from "@/components/time-of-day-icon.vue"
import NavIcon from "@/components/nav-icon.vue"

const NOTIFICATIONS_PAGE_SIZE = 20

const router = useRouter()

const authStore = useAuthStore()
const systemNotificationStore = useSystemNotificationStore()
const notificationStore = useNotificationStore()
const { user } = storeToRefs(authStore)
const { unreadNotifications } = storeToRefs(systemNotificationStore)
const { notifications: mentions } = storeToRefs(notificationStore)

onMounted(() => {
  systemNotificationStore.fetchUnreadNotifications(NOTIFICATIONS_PAGE_SIZE, 0)
  notificationStore.fetchNotifications(NOTIFICATIONS_PAGE_SIZE, 0)
})

async function markNotificationRead(id: number) {
  try {
    await systemNotificationStore.markNotificationRead(id)
  } catch {
    notify.error("Не удалось скрыть уведомление")
  }
}

async function hideMention(id: number) {
  try {
    await notificationStore.hideNotification(id)
  } catch {
    notify.error("Не удалось скрыть уведомление")
  }
}

function openMention(chatId: number, messageId: number) {
  router.push({ path: `/chats/${chatId}`, query: { message: String(messageId) } })
}

const now = new Date()
const period = getDayPeriod(now.getHours())

const greeting = computed(() => (user.value ? getGreeting(shortName(user.value)) : ""))
const today = formatFullDate(now)

const sunIcon = ref<InstanceType<typeof TimeOfDayIcon> | null>(null)
const isSunLaunched = computed(() => sunIcon.value?.launched ?? false)

function handleSunClick() {
  sunIcon.value?.boost()
}
</script>

<template>
  <div class="flex min-h-full flex-col items-center justify-center gap-8 p-6 sm:gap-10 sm:p-10">
    <div class="flex animate-rise flex-col items-center gap-6 text-center">
      <div
        class="relative flex h-32 w-32 cursor-pointer items-center justify-center"
        @click="handleSunClick"
      >
        <div
          class="absolute inset-0 rounded-full bg-accent/25 blur-2xl transition-opacity duration-700"
          :class="isSunLaunched ? 'opacity-0' : 'opacity-100'"
        ></div>
        <div
          class="glass hairline absolute inset-2 rounded-full transition-opacity duration-700"
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

      <div class="flex flex-col gap-2">
        <h1
          class="gradient-text m-0 text-2xl font-semibold tracking-tight text-balance sm:text-4xl"
        >
          {{ greeting }}
        </h1>
        <span
          class="glass hairline mx-auto rounded-full px-3.5 py-1 text-xs font-medium text-second sm:text-sm"
        >
          {{ today }}
        </span>
      </div>
    </div>

    <div v-if="mentions.length > 0" class="flex w-full max-w-3xl flex-col gap-3">
      <div
        v-for="(mention, index) in mentions"
        :key="mention.id"
        class="glass hairline shadow-card group flex animate-rise cursor-pointer items-start gap-4 rounded-card px-5 py-4 text-left transition-[transform,box-shadow] duration-300 hover:-translate-y-0.5 hover:shadow-float"
        :style="{ animationDelay: `${index * 80}ms` }"
        @click="openMention(mention.message.chat.id, mention.message.id)"
      >
        <span
          class="chip-accent glow-accent-soft flex h-11 w-11 shrink-0 items-center justify-center"
        >
          <NavIcon name="chats" />
        </span>
        <span class="flex min-w-0 flex-1 flex-col gap-1">
          <span class="text-[15px] font-semibold text-main">
            {{ shortName(mention.message.user) }} упомянул вас
          </span>
          <span class="truncate text-sm text-second">{{ mention.message.text }}</span>
          <span class="flex flex-wrap items-center gap-2 text-xs text-second/80">
            {{ mention.message.chat.title }}
            <span>·</span>
            {{ formatDateTime(mention.message.createdAt) }}
          </span>
        </span>
        <button
          type="button"
          class="press flex h-9 w-9 shrink-0 cursor-pointer items-center justify-center rounded-full text-second opacity-60 hover:bg-main/6 hover:text-main group-hover:opacity-100"
          title="Скрыть"
          aria-label="Скрыть"
          @click.stop="hideMention(mention.id)"
        >
          <NavIcon name="cancel" :size="16" />
        </button>
      </div>
    </div>

    <div v-if="unreadNotifications.length > 0" class="flex w-full max-w-3xl flex-col gap-3">
      <div
        v-for="(notification, index) in unreadNotifications"
        :key="notification.id"
        class="glass hairline shadow-card group flex animate-rise items-start gap-4 rounded-card px-5 py-4 transition-[transform,box-shadow] duration-300 hover:-translate-y-0.5 hover:shadow-float"
        :style="{ animationDelay: `${index * 80}ms` }"
      >
        <span
          class="chip-accent glow-accent-soft flex h-11 w-11 shrink-0 items-center justify-center"
        >
          <NavIcon name="bell" />
        </span>
        <span class="flex min-w-0 flex-1 flex-col gap-1">
          <span class="text-[15px] font-semibold text-main">{{ notification.title }}</span>
          <span class="text-sm whitespace-pre-wrap text-second">{{ notification.text }}</span>
          <span class="text-xs text-second/80">{{ formatDateTime(notification.createdAt) }}</span>
        </span>
        <button
          type="button"
          class="press flex h-9 w-9 shrink-0 cursor-pointer items-center justify-center rounded-full text-second opacity-60 hover:bg-main/6 hover:text-main group-hover:opacity-100"
          title="Скрыть"
          aria-label="Скрыть"
          @click="markNotificationRead(notification.id)"
        >
          <NavIcon name="cancel" :size="16" />
        </button>
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
