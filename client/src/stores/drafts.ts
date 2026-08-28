import { defineStore } from "pinia"
import { useStorage } from "@vueuse/core"

export const useDraftStore = defineStore("drafts", () => {
  const drafts = useStorage<Record<number, string>>("chatDrafts", {})

  function getDraft(chatId: number) {
    return drafts.value[chatId] ?? ""
  }

  function setDraft(chatId: number, text: string) {
    if (text.trim() === "") {
      delete drafts.value[chatId]
    } else {
      drafts.value[chatId] = text
    }
  }

  return { drafts, getDraft, setDraft }
})
