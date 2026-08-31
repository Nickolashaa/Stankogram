import { defineStore } from "pinia"
import { computed, ref } from "vue"
import { apolloClient } from "@/api"
import { CreateSystemNotificationDocument } from "@/graphql/mutations/system-notifications/create-system-notification.generated"
import { UpdateSystemNotificationDocument } from "@/graphql/mutations/system-notifications/update-system-notification.generated"
import { MarkSystemNotificationReadDocument } from "@/graphql/mutations/system-notifications/mark-system-notification-read.generated"
import { MeSystemNotificationsDocument } from "@/graphql/queries/system-notifications/me-system-notifications.generated"
import { SystemNotificationsDocument } from "@/graphql/queries/system-notifications/system-notifications.generated"
import type { SystemNotificationFieldsFragment } from "@/graphql/fragments/system-notifications.generated"
import type { SystemNotificationIn } from "@/graphql/base-types"

export const useSystemNotificationStore = defineStore("systemNotifications", () => {
  const unreadNotifications = ref<SystemNotificationFieldsFragment[]>([])

  const notifications = ref<SystemNotificationFieldsFragment[]>([])
  const totalCount = ref(0)

  const hasUnread = computed(() => unreadNotifications.value.length > 0)

  async function fetchUnreadNotifications(limit: number, offset: number) {
    const { data } = await apolloClient.query({
      query: MeSystemNotificationsDocument,
      variables: { filters: { onlyUnread: true }, pagination: { limit, offset } },
      fetchPolicy: "network-only",
    })

    unreadNotifications.value = data.meSystemNotifications.systemNotifications
  }

  async function fetchNotifications(
    limit: number,
    offset: number,
    options: { append?: boolean } = {},
  ) {
    const { data } = await apolloClient.query({
      query: SystemNotificationsDocument,
      variables: { pagination: { limit, offset } },
      fetchPolicy: "network-only",
    })

    notifications.value = options.append
      ? [...notifications.value, ...data.systemNotifications.systemNotifications]
      : data.systemNotifications.systemNotifications
    totalCount.value = data.systemNotifications.count
  }

  async function createNotification(input: SystemNotificationIn) {
    const { data } = await apolloClient.mutate({
      mutation: CreateSystemNotificationDocument,
      variables: { input },
    })

    if (data === undefined || data === null) {
      throw new Error("Failed to create system notification")
    }
  }

  async function updateNotification(id: number, input: SystemNotificationIn) {
    const { data } = await apolloClient.mutate({
      mutation: UpdateSystemNotificationDocument,
      variables: { id, input },
    })

    const result = data?.updateSystemNotification

    if (result?.__typename !== "SystemNotification") {
      throw new Error(result?.message ?? "Failed to update system notification")
    }
  }

  async function markNotificationRead(id: number) {
    const { data } = await apolloClient.mutate({
      mutation: MarkSystemNotificationReadDocument,
      variables: { id },
    })

    const result = data?.markSystemNotificationRead

    if (result != null) {
      throw new Error(result.message)
    }

    unreadNotifications.value = unreadNotifications.value.filter((item) => item.id !== id)
  }

  return {
    unreadNotifications,
    notifications,
    totalCount,
    hasUnread,
    fetchUnreadNotifications,
    fetchNotifications,
    createNotification,
    updateNotification,
    markNotificationRead,
  }
})
