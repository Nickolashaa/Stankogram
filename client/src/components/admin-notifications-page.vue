<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import { storeToRefs } from "pinia"
import { useSystemNotificationStore } from "@/stores/system-notifications"
import { formatDateTime, isExpired } from "@/lib/format"
import { pinForLeave } from "@/lib/transition"
import { notify } from "@/lib/notify"
import type { SystemNotificationIn } from "@/graphql/base-types"
import type { SystemNotificationFieldsFragment } from "@/graphql/fragments/system-notifications.generated"
import Button from "@/components/button.vue"
import NavIcon from "@/components/nav-icon.vue"
import AdminPage from "@/components/admin-page.vue"
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

async function loadMore() {
  await notificationStore.fetchNotifications(PAGE_SIZE, notifications.value.length, {
    append: true,
  })
}

const canLoadMore = computed(() => !loading.value && notifications.value.length < totalCount.value)

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
}
</script>

<template>
  <AdminPage
    title="Системные уведомления"
    :total="totalCount"
    :can-load-more="canLoadMore"
    :load-more="loadMore"
  >
    <template #actions>
      <Button icon="plus" :short-mode="false" class="w-full sm:w-auto" @click="openCreateDialog"
        >Создать уведомление</Button
      >
    </template>

    <div class="relative flex flex-col gap-3">
      <TransitionGroup name="row" @before-leave="pinForLeave">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="glass hairline shadow-card flex items-start gap-4 rounded-card px-5 py-4 transition-[transform,box-shadow] duration-300 hover:-translate-y-0.5 hover:shadow-float"
        >
          <span
            class="chip-accent glow-accent-soft flex h-11 w-11 shrink-0 items-center justify-center"
          >
            <NavIcon name="bell" :size="18" />
          </span>
          <div class="flex min-w-0 flex-1 flex-col gap-1">
            <span class="text-[15px] font-semibold text-main">{{ notification.title }}</span>
            <span class="text-sm whitespace-pre-wrap text-second">{{ notification.text }}</span>
            <span class="flex flex-wrap items-center gap-2 text-xs text-second">
              {{ formatDateTime(notification.createdAt) }}
              <span
                v-if="notification.expiresAt !== null && notification.expiresAt !== undefined"
                class="inline-flex shrink-0 items-center rounded-full px-2.5 py-0.5 text-xs font-medium whitespace-nowrap"
                :class="
                  isExpired(notification.expiresAt)
                    ? 'bg-red-500/12 text-red-600 ring-1 ring-red-500/25 ring-inset dark:text-red-400'
                    : 'bg-accent/15 text-accent ring-1 ring-accent/25 ring-inset'
                "
              >
                {{
                  isExpired(notification.expiresAt)
                    ? `Истекло ${formatDateTime(notification.expiresAt)}`
                    : `До ${formatDateTime(notification.expiresAt)}`
                }}
              </span>
            </span>
          </div>
          <Button
            icon="edit"
            variant="ghost"
            title="Редактировать"
            aria-label="Редактировать"
            @click="openEditDialog(notification)"
          />
        </div>
      </TransitionGroup>

      <div
        v-if="notifications.length === 0 && !loading"
        class="glass hairline shadow-card rounded-card px-5 py-10 text-center text-sm text-second"
      >
        Уведомлений пока нет
      </div>
    </div>

    <AdminNotificationFormDialog
      :open="dialogOpen"
      :title="dialogMode === 'create' ? 'Новое уведомление' : 'Редактирование уведомления'"
      :initial-notification="editingNotification"
      :submitting="saving"
      @close="dialogOpen = false"
      @submit="handleSubmit"
    />
  </AdminPage>
</template>
