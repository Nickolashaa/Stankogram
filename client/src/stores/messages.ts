import { defineStore } from "pinia"
import { ref } from "vue"
import { apolloClient } from "@/api"
import { CreateMessageDocument } from "@/graphql/mutations/messages/create-message.generated"
import { MessagesDocument } from "@/graphql/queries/messages/messages.generated"
import type { MessageFieldsFragment } from "@/graphql/fragments/messages.generated"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import { EMessageType } from "@/graphql/base-types"

export type MessageItem = MessageFieldsFragment & { user: UserFieldsFragment }

export const useMessageStore = defineStore("messages", () => {
  const chatId = ref<number | null>(null)
  const messages = ref<MessageItem[]>([])
  const totalCount = ref(0)

  function openChat(id: number) {
    chatId.value = id
    messages.value = []
    totalCount.value = 0
  }

  async function fetchMessages(limit: number, offset: number, options: { append?: boolean } = {}) {
    if (chatId.value === null) {
      return
    }

    const activeChatId = chatId.value
    const { data } = await apolloClient.query({
      query: MessagesDocument,
      variables: { filters: { chatId: activeChatId }, pagination: { limit, offset } },
      fetchPolicy: "network-only",
    })

    if (chatId.value !== activeChatId) {
      return
    }

    messages.value = options.append
      ? [...messages.value, ...data.messages.messages]
      : data.messages.messages
    totalCount.value = data.messages.count
  }

  async function sendMessage(text: string) {
    if (chatId.value === null) {
      return
    }

    const { data } = await apolloClient.mutate({
      mutation: CreateMessageDocument,
      variables: { input: { chatId: chatId.value, type: EMessageType.Text, text } },
    })

    if (data === undefined || data === null || data.createMessage.__typename !== "Message") {
      throw new Error(data?.createMessage.message ?? "Failed to send message")
    }
  }

  function handleIncomingMessage(message: MessageItem & { chat: { id: number } }) {
    if (chatId.value === null || message.chat.id !== chatId.value) {
      return
    }

    messages.value = [message, ...messages.value]
    totalCount.value += 1
  }

  return {
    chatId,
    messages,
    totalCount,
    openChat,
    fetchMessages,
    sendMessage,
    handleIncomingMessage,
  }
})
