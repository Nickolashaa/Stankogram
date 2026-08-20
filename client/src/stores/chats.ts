import { defineStore } from "pinia"
import { ref } from "vue"
import { client } from "./../api"
import type { components } from "./../api/schema"

type ChatProfileResponse = components["schemas"]["ChatProfileResponse"]

export const useChatStore = defineStore("chats", () => {
  const chats = ref<ChatProfileResponse[]>([])

  async function fetchChats() {
    const { data } = await client.GET("/api/chats")
    chats.value = data ?? []
  }

  async function getOrCreatePrivateChat(participantId: number) {
    const { data, error } = await client.POST("/api/chats/private/get_or_create", {
      body: participantId,
    })

    if (error !== undefined) {
      throw new Error(error.detail?.toString())
    }

    return data
  }

  return {
    chats,
    fetchChats,
    getOrCreatePrivateChat,
  }
})
