import { defineStore } from "pinia"
import { ref } from "vue"
import { apolloClient } from "@/api"
import { CreateMessageDocument } from "@/graphql/mutations/messages/create-message.generated"
import { UpdateMessageDocument } from "@/graphql/mutations/messages/update-message.generated"
import { DeleteMessageDocument } from "@/graphql/mutations/messages/delete-message.generated"
import { MessagesDocument } from "@/graphql/queries/messages/messages.generated"
import { MessagePositionDocument } from "@/graphql/queries/messages/message-position.generated"
import type { MessageFieldsFragment } from "@/graphql/fragments/messages.generated"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"

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

  async function fetchMessagePosition(messageId: number) {
    const { data } = await apolloClient.query({
      query: MessagePositionDocument,
      variables: { messageId },
      fetchPolicy: "network-only",
    })

    return data.messagePosition
  }

  async function sendMessage(text: string, mentionedUserIds: number[]) {
    if (chatId.value === null) {
      return
    }

    const { data } = await apolloClient.mutate({
      mutation: CreateMessageDocument,
      variables: { input: { chatId: chatId.value, text, mentionedUserIds } },
    })

    if (data === undefined || data === null || data.createMessage.__typename !== "Message") {
      throw new Error(data?.createMessage.message ?? "Failed to send message")
    }
  }

  async function updateMessage(messageId: number, text: string, mentionedUserIds: number[]) {
    const { data } = await apolloClient.mutate({
      mutation: UpdateMessageDocument,
      variables: { messageId, input: { text, mentionedUserIds } },
    })

    if (data === undefined || data === null || data.updateMessage.__typename !== "Message") {
      throw new Error(data?.updateMessage.message ?? "Failed to update message")
    }
  }

  async function deleteMessage(messageId: number) {
    const { data } = await apolloClient.mutate({
      mutation: DeleteMessageDocument,
      variables: { messageId },
    })

    if (data === undefined || data === null || data.deleteMessage.__typename !== "Message") {
      throw new Error(data?.deleteMessage.message ?? "Failed to delete message")
    }
  }

  function handleCreateMessage(message: MessageItem & { chat: { id: number } }) {
    if (chatId.value === null || message.chat.id !== chatId.value) {
      return
    }

    messages.value = [message, ...messages.value]
    totalCount.value += 1
  }

  function handleUpdateMessage(message: MessageItem & { chat: { id: number } }) {
    if (chatId.value === null || message.chat.id !== chatId.value) {
      return
    }

    messages.value = messages.value.map((item) =>
      item.id === message.id ? { ...item, ...message } : item,
    )
  }

  function handleDeleteMessage(message: { id: number; chat: { id: number } }) {
    if (chatId.value === null || message.chat.id !== chatId.value) {
      return
    }
    if (!messages.value.some((item) => item.id === message.id)) {
      return
    }

    messages.value = messages.value.filter((item) => item.id !== message.id)
    totalCount.value = Math.max(0, totalCount.value - 1)
  }

  return {
    chatId,
    messages,
    totalCount,
    openChat,
    fetchMessages,
    fetchMessagePosition,
    sendMessage,
    updateMessage,
    deleteMessage,
    handleCreateMessage,
    handleUpdateMessage,
    handleDeleteMessage,
  }
})
