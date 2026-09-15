import { defineStore } from "pinia"
import { ref } from "vue"
import { apolloClient } from "@/api"
import { MeNotificationsDocument } from "@/graphql/queries/notifications/me-notifications.generated"
import { HideNotificationDocument } from "@/graphql/mutations/notifications/hide-notification.generated"
import type { MeNotificationsQuery } from "@/graphql/queries/notifications/me-notifications.generated"

export type NotificationItem = MeNotificationsQuery["meNotifications"]["notifications"][number]

export const useNotificationStore = defineStore("notifications", () => {
  const notifications = ref<NotificationItem[]>([])
  const totalCount = ref(0)

  async function fetchNotifications(limit: number, offset: number) {
    const { data } = await apolloClient.query({
      query: MeNotificationsDocument,
      variables: { pagination: { limit, offset } },
      fetchPolicy: "network-only",
    })

    notifications.value = data.meNotifications.notifications
    totalCount.value = data.meNotifications.count
  }

  async function hideNotification(id: number) {
    const { data } = await apolloClient.mutate({
      mutation: HideNotificationDocument,
      variables: { id },
    })

    const result = data?.hideNotification

    if (result != null) {
      throw new Error(result.message)
    }

    notifications.value = notifications.value.filter((item) => item.id !== id)
    totalCount.value = Math.max(totalCount.value - 1, 0)
  }

  return {
    notifications,
    totalCount,
    fetchNotifications,
    hideNotification,
  }
})
