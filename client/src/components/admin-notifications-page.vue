<script setup lang="ts">
import { onMounted, ref } from "vue"
import { storeToRefs } from "pinia"
import { useInfiniteScroll } from "@vueuse/core"
import { useSystemNotificationStore } from "@/stores/system-notifications"
import { formatDateTime } from "@/lib/format"
import { notify } from "@/lib/notify"
import type { SystemNotificationIn } from "@/graphql/base-types"
import type { SystemNotificationFieldsFragment } from "@/graphql/fragments/system-notifications.generated"
import Button from "@/components/button.vue"
import NavIcon from "@/components/nav-icon.vue"
import AdminNotificationFormDialog from "@/components/admin-notification-form-dialog.vue"

const PAGE_SIZE = 20

const notificationStore = useSystemNotificationStore()
const { notifications, totalCount } = storeToRefs(notificationStore)

const loading = ref(false)

async function fetchNotifications() {
  loading.value = true
  try {
    await notificationStore.fetchNotifications(PAGE_SIZE, 0)
  } finally {
    loading.value = false
  }
}

const infiniteScroll = useInfiniteScroll(
  window,
  async () => {
    await notificationStore.fetchNotifications(PAGE_SIZE, notifications.value.length, {
      append: true,
    })
  },
  {
    distance: 200,
    canLoadMore: () => !loading.value && notifications.value.length < totalCount.value,
  },
)

onMounted(fetchNotifications)

const dialogOpen = ref(false)
const dialogMode = ref<"create" | "edit">("create")
const editingNotification = ref<SystemNotificationFieldsFragment | null>(null)
const saving = ref(false)

function openCreateDialog() {
  dialogMode.value = "create"
  editingNotification.value = null
  dialogOpen.value = true
}

function openEditDialog(notification: SystemNotificationFieldsFragment) {
  dialogMode.value = "edit"
  editingNotification.value = notification
  dialogOpen.value = true
}

async function handleSubmit(data: SystemNotificationIn) {
  saving.value = true
  try {
    if (dialogMode.value === "create") {
      await notificationStore.createNotification(data)
      notify.success("Уведомление опубликовано")
    } else if (editingNotification.value !== null) {
      await notificationStore.updateNotification(editingNotification.value.id, data)
      notify.success("Уведомление обновлено")
    }
  } catch {
    notify.error("Не удалось сохранить уведомление")
    return
  } finally {
    saving.value = false
  }

  dialogOpen.value = false
  await fetchNotifications()
  infiniteScroll.reset()
}
</script>

<template>
  <div class="flex animate-appear flex-col gap-6">
    <div class="flex flex-col items-start gap-3 sm:flex-row sm:items-center sm:justify-between">
      <h1 class="m-0 text-2xl font-semibold text-main">Системные уведомления</h1>
      <Button icon="plus" :short-mode="false" class="w-full sm:w-auto" @click="openCreateDialog"
        >Создать уведомление</Button
      >
    </div>

    <div class="flex flex-col gap-3">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="flex items-start gap-4 rounded-card bg-card px-5 py-4 shadow-card"
      >
        <span
          class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-accent/10 text-accent"
        >
          <NavIcon name="bell" :size="18" />
        </span>
        <div class="flex min-w-0 flex-1 flex-col gap-1">
          <span class="text-[15px] whitespace-pre-wrap text-main">{{ notification.text }}</span>
          <span class="text-xs text-second">{{ formatDateTime(notification.createdAt) }}</span>
        </div>
        <Button
          icon="edit"
          variant="ghost"
          title="Редактировать"
          aria-label="Редактировать"
          @click="openEditDialog(notification)"
        />
      </div>

      <div
        v-if="notifications.length === 0 && !loading"
        class="rounded-card bg-card px-5 py-8 text-center text-sm text-second shadow-card"
      >
        Уведомлений пока нет
      </div>
    </div>

    <div class="flex items-center justify-between text-sm text-second">
      <span>Всего: {{ totalCount }}</span>
      <span v-if="infiniteScroll.isLoading.value">Загрузка...</span>
    </div>

    <AdminNotificationFormDialog
      :open="dialogOpen"
      :title="dialogMode === 'create' ? 'Новое уведомление' : 'Редактирование уведомления'"
      :initial-notification="editingNotification"
      :submitting="saving"
      @close="dialogOpen = false"
      @submit="handleSubmit"
    />
  </div>
</template>
