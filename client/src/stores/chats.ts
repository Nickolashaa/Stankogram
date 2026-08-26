import { defineStore } from "pinia"
import { ref } from "vue"
import { apolloClient } from "@/api"
import { CreatePrivateChatDocument } from "@/graphql/mutations/chats/create-private-chat.generated"
import { MeChatsDocument } from "@/graphql/queries/chats/me-chats.generated"
import type { ChatFieldsFragment } from "@/graphql/fragments/chats.generated"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import type { MessageFieldsFragment } from "@/graphql/fragments/messages.generated"
import { EChatType, type ChatFiltersIn } from "@/graphql/base-types"

const RESYNC_PAGE_SIZE = 30

export type ChatSummary = ChatFieldsFragment & {
  recipients: UserFieldsFragment[]
  lastMessage: (MessageFieldsFragment & { user: UserFieldsFragment }) | null
}

export const useChatStore = defineStore("chats", () => {
  const chats = ref<ChatSummary[]>([])
  const totalCount = ref(0)

  async function fetchChats(
    filters: ChatFiltersIn | undefined,
    limit: number,
    offset: number,
    options: { append?: boolean } = {},
  ) {
    const { data } = await apolloClient.query({
      query: MeChatsDocument,
      variables: { filters, pagination: { limit, offset } },
      fetchPolicy: "network-only",
    })

    if (data.meChats.__typename !== "ChatsMeta") {
      return
    }

    chats.value = options.append ? [...chats.value, ...data.meChats.chats] : data.meChats.chats
    totalCount.value = data.meChats.count
  }

  async function startPrivateChat(participantId: number): Promise<number> {
    const { data } = await apolloClient.mutate({
      mutation: CreatePrivateChatDocument,
      variables: { input: { participantId } },
    })

    const result = data?.createPrivateChat

    if (result?.__typename === "Chat") {
      if (!chats.value.some((item) => item.id === result.id)) {
        chats.value = [result, ...chats.value]
        totalCount.value += 1
      }
      return result.id
    }

    if (result?.__typename === "ObjectAlreadyExistsError") {
      const existing = await apolloClient.query({
        query: MeChatsDocument,
        variables: { filters: { type: EChatType.Private }, pagination: { limit: 100, offset: 0 } },
        fetchPolicy: "network-only",
      })
      const existingMeChats = existing.data.meChats
      if (existingMeChats.__typename === "ChatsMeta") {
        const found = existingMeChats.chats.find((chat: ChatSummary) =>
          chat.recipients.some((recipient) => recipient.id === participantId),
        )
        if (found) {
          return found.id
        }
      }
    }

    throw new Error(result?.message ?? "Failed to start chat")
  }

  function handleIncomingMessage(
    message: MessageFieldsFragment & { user: UserFieldsFragment; chat: { id: number } },
  ) {
    const index = chats.value.findIndex((chat) => chat.id === message.chat.id)

    if (index === -1) {
      fetchChats(undefined, RESYNC_PAGE_SIZE, 0)
      return
    }

    const current = chats.value[index]
    if (current === undefined) {
      return
    }

    const updated: ChatSummary = { ...current, lastMessage: message }
    const rest = [...chats.value]
    rest.splice(index, 1)
    chats.value = [updated, ...rest]
  }

  return {
    chats,
    totalCount,
    fetchChats,
    startPrivateChat,
    handleIncomingMessage,
  }
})
