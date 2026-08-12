import { defineStore } from "pinia"
import { ref } from "vue"
import { client } from "./../api"
import type { components } from "./../api/schema"

type MessageResponse = components["schemas"]["MessageResponse"]

export const useMessageStore = defineStore("messages", () => {
  const messages = ref<MessageResponse[]>([])

  async function fetchMessages(chatId: number) {
    const { data } = await client.GET("/api/messages", {
      params: { query: { chat_id: chatId } },
    })
    messages.value = (data ?? []).slice().reverse()
  }

  async function sendMessage(chatId: number, text: string) {
    const { data, error } = await client.POST("/api/messages/create", {
      body: { chat_id: chatId, type: "TEXT", text },
    })

    if (error !== undefined) {
      throw new Error(error.detail?.toString())
    }

    messages.value.push(data)

    return data
  }

  return {
    messages,
    fetchMessages,
    sendMessage,
  }
})
