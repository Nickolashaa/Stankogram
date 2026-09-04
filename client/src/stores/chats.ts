import { defineStore } from "pinia"
import { computed, ref, type Ref } from "vue"
import { apolloClient } from "@/api"
import { useAuthStore } from "@/stores/auth"
import { CreatePrivateChatDocument } from "@/graphql/mutations/chats/create-private-chat.generated"
import { CreatePublicChatDocument } from "@/graphql/mutations/chats/create-public-chat.generated"
import { UpdateChatDocument } from "@/graphql/mutations/chats/update-chat.generated"
import { AddParticipantToChatDocument } from "@/graphql/mutations/chats/add-participant-to-chat.generated"
import { RemoveParticipantFromChatDocument } from "@/graphql/mutations/chats/remove-participant-from-chat.generated"
import { LeaveChatDocument } from "@/graphql/mutations/chats/leave-chat.generated"
import { DeleteChatDocument } from "@/graphql/mutations/chats/delete-chat.generated"
import { UpdateChatParticipantPermissionsDocument } from "@/graphql/mutations/chats/update-chat-participant-permissions.generated"
import { MarkChatReadDocument } from "@/graphql/mutations/chats/mark-chat-read.generated"
import { MeChatsDocument } from "@/graphql/queries/chats/me-chats.generated"
import { ChatsDocument } from "@/graphql/queries/chats/chats.generated"
import type { ChatFieldsFragment } from "@/graphql/fragments/chats.generated"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import type { MessageFieldsFragment } from "@/graphql/fragments/messages.generated"
import { EChatType, type ChatFiltersIn } from "@/graphql/base-types"

const RESYNC_PAGE_SIZE = 30

export type ChatParticipantItem = {
  id: number
  isAdmin: boolean
  isMuted: boolean
  lastReadAt: string | null
  user: UserFieldsFragment
}

export type ChatSummary = ChatFieldsFragment & {
  participants: ChatParticipantItem[]
  lastMessage: (MessageFieldsFragment & { user: UserFieldsFragment }) | null
}

export function hasUnreadMessages(chat: ChatSummary, currentUserId: number): boolean {
  if (chat.lastMessage === null || chat.lastMessage.user.id === currentUserId) {
    return false
  }
  const participant = chat.participants.find((item) => item.user.id === currentUserId)
  if (participant === undefined) {
    return false
  }
  if (participant.lastReadAt === null) {
    return true
  }
  return new Date(chat.lastMessage.createdAt) > new Date(participant.lastReadAt)
}

export const useChatStore = defineStore("chats", () => {
  const authStore = useAuthStore()

  const chats = ref<ChatSummary[]>([])
  const totalCount = ref(0)

  const hasUnread = computed(() => {
    const currentUser = authStore.user
    if (currentUser === undefined) {
      return false
    }
    return chats.value.some((chat) => hasUnreadMessages(chat, currentUser.id))
  })

  const adminChats = ref<ChatSummary[]>([])
  const adminTotalCount = ref(0)

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

  async function fetchAdminChats(
    filters: ChatFiltersIn | undefined,
    limit: number,
    offset: number,
    options: { append?: boolean } = {},
  ) {
    const { data } = await apolloClient.query({
      query: ChatsDocument,
      variables: { filters, pagination: { limit, offset } },
      fetchPolicy: "network-only",
    })

    adminChats.value = options.append
      ? [...adminChats.value, ...data.chats.chats]
      : data.chats.chats
    adminTotalCount.value = data.chats.count
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
          chat.participants.some((participant) => participant.user.id === participantId),
        )
        if (found) {
          return found.id
        }
      }
    }

    throw new Error(result?.message ?? "Failed to start chat")
  }

  function patchChatIn(list: Ref<ChatSummary[]>, chatId: number, patch: Partial<ChatSummary>) {
    const index = list.value.findIndex((chat) => chat.id === chatId)
    const current = list.value[index]
    if (current === undefined) {
      return
    }
    const rest = [...list.value]
    rest[index] = { ...current, ...patch }
    list.value = rest
  }

  function patchChat(chatId: number, patch: Partial<ChatSummary>) {
    patchChatIn(chats, chatId, patch)
    patchChatIn(adminChats, chatId, patch)
  }

  function patchParticipantIn(
    list: Ref<ChatSummary[]>,
    chatId: number,
    participant: ChatParticipantItem,
  ) {
    const chat = list.value.find((item) => item.id === chatId)
    if (chat === undefined) {
      return
    }
    const index = chat.participants.findIndex((item) => item.user.id === participant.user.id)
    const participants =
      index === -1
        ? [...chat.participants, participant]
        : chat.participants.map((item, i) => (i === index ? participant : item))
    patchChatIn(list, chatId, { participants })
  }

  function patchParticipant(chatId: number, participant: ChatParticipantItem) {
    patchParticipantIn(chats, chatId, participant)
    patchParticipantIn(adminChats, chatId, participant)
  }

  function removeChatIn(list: Ref<ChatSummary[]>, total: Ref<number>, chatId: number) {
    if (!list.value.some((chat) => chat.id === chatId)) {
      return
    }
    list.value = list.value.filter((chat) => chat.id !== chatId)
    total.value = Math.max(0, total.value - 1)
  }

  function removeParticipantIn(list: Ref<ChatSummary[]>, chatId: number, userId: number) {
    const chat = list.value.find((item) => item.id === chatId)
    if (chat === undefined) {
      return
    }
    patchChatIn(list, chatId, {
      participants: chat.participants.filter((p) => p.user.id !== userId),
    })
  }

  async function createGroupChat(title: string, participantIds: number[]): Promise<number> {
    const { data } = await apolloClient.mutate({
      mutation: CreatePublicChatDocument,
      variables: { input: { title, participantIds } },
    })

    const result = data?.createPublicChat

    if (result?.__typename === "Chat") {
      chats.value = [result, ...chats.value]
      totalCount.value += 1
      return result.id
    }

    throw new Error(result?.message ?? "Failed to create chat")
  }

  async function updateChatTitle(chatId: number, title: string) {
    const { data } = await apolloClient.mutate({
      mutation: UpdateChatDocument,
      variables: { chatId, input: { title } },
    })

    const result = data?.updateChat

    if (result?.__typename !== "Chat") {
      throw new Error(result?.message ?? "Failed to update chat")
    }

    patchChat(chatId, { title: result.title })
  }

  async function addParticipant(chatId: number, userId: number) {
    const { data } = await apolloClient.mutate({
      mutation: AddParticipantToChatDocument,
      variables: { input: { chatId, userId, isAdmin: false, isMuted: false } },
    })

    const result = data?.addParticipantToChat

    if (result?.__typename !== "ChatParticipant") {
      throw new Error(result?.message ?? "Failed to add participant")
    }

    patchParticipant(chatId, result)
  }

  async function removeParticipant(chatId: number, userId: number) {
    await apolloClient.mutate({
      mutation: RemoveParticipantFromChatDocument,
      variables: { chatId, userId },
    })

    removeParticipantIn(chats, chatId, userId)
    removeParticipantIn(adminChats, chatId, userId)
  }

  async function leaveChat(chatId: number) {
    const { data } = await apolloClient.mutate({
      mutation: LeaveChatDocument,
      variables: { chatId },
    })

    const result = data?.leaveChat

    if (result?.__typename !== "Chat") {
      throw new Error(result?.message ?? "Failed to leave chat")
    }

    removeChatIn(chats, totalCount, chatId)

    const currentUser = authStore.user
    if (currentUser !== undefined) {
      removeParticipantIn(adminChats, chatId, currentUser.id)
    }
  }

  async function deleteChat(chatId: number) {
    const { data } = await apolloClient.mutate({
      mutation: DeleteChatDocument,
      variables: { chatId },
    })

    const result = data?.deleteChat

    if (result?.__typename !== "Chat") {
      throw new Error(result?.message ?? "Failed to delete chat")
    }

    removeChatIn(chats, totalCount, chatId)
    removeChatIn(adminChats, adminTotalCount, chatId)
  }

  async function setParticipantPermissions(
    chatId: number,
    userId: number,
    isAdmin: boolean,
    isMuted: boolean,
  ) {
    const { data } = await apolloClient.mutate({
      mutation: UpdateChatParticipantPermissionsDocument,
      variables: { input: { chatId, userId, isAdmin, isMuted } },
    })

    const result = data?.updateChatParticipantPermissions

    if (result?.__typename !== "ChatParticipant") {
      throw new Error(result?.message ?? "Failed to update participant")
    }

    patchParticipant(chatId, result)
  }

  async function markChatRead(chatId: number) {
    const currentUserId = authStore.user?.id
    const local = chats.value
      .find((chat) => chat.id === chatId)
      ?.participants.find((item) => item.user.id === currentUserId)

    if (local !== undefined) {
      patchParticipant(chatId, { ...local, lastReadAt: new Date().toISOString() })
    }

    const { data } = await apolloClient.mutate({
      mutation: MarkChatReadDocument,
      variables: { chatId },
    })

    const result = data?.markChatRead

    if (result?.__typename !== "ChatParticipant") {
      return
    }

    patchParticipant(chatId, result)
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
    hasUnread,
    adminChats,
    adminTotalCount,
    fetchChats,
    fetchAdminChats,
    startPrivateChat,
    createGroupChat,
    updateChatTitle,
    addParticipant,
    removeParticipant,
    leaveChat,
    deleteChat,
    setParticipantPermissions,
    markChatRead,
    handleIncomingMessage,
  }
})
