<script setup lang="ts">
import { nextTick, ref, watch } from "vue"
import type { components } from "@/api/schema"
import Input from "@/components/input.vue"
import Button from "@/components/button.vue"

type MessageResponse = components["schemas"]["MessageResponse"]

const props = defineProps<{
  title: string
  messages: MessageResponse[]
  currentUserId: number
  sending: boolean
}>()

const emit = defineEmits<{
  send: [text: string]
}>()

const text = ref("")
const scrollRef = ref<HTMLElement | null>(null)

function formatTime(value: string) {
  return new Date(value).toLocaleString("ru-RU", { timeStyle: "short" })
}

function handleSubmit() {
  const value = text.value.trim()
  if (value === "") {
    return
  }

  emit("send", value)
  text.value = ""
}

watch(
  () => props.messages.length,
  async () => {
    await nextTick()
    scrollRef.value?.scrollTo({ top: scrollRef.value.scrollHeight })
  },
)
</script>

<template>
  <div class="flex flex-1 flex-col">
    <div class="border-b border-second/15 px-6 py-4">
      <h2 class="m-0 text-lg font-semibold text-main">{{ title }}</h2>
    </div>

    <div ref="scrollRef" class="flex flex-1 flex-col gap-3 overflow-y-auto px-6 py-4">
      <div
        v-for="message in messages"
        :key="message.id"
        class="flex flex-col"
        :class="message.user_id === currentUserId ? 'items-end' : 'items-start'"
      >
        <div
          class="max-w-md rounded-card px-4 py-2.5 text-[15px]"
          :class="
            message.user_id === currentUserId ? 'bg-accent text-bg' : 'bg-card text-main shadow-card'
          "
        >
          {{ message.text }}
        </div>
        <span class="mt-1 text-xs text-second">{{ formatTime(message.created_at) }}</span>
      </div>

      <div v-if="messages.length === 0" class="flex flex-1 items-center justify-center text-second">
        Сообщений пока нет
      </div>
    </div>

    <form class="flex items-center gap-3 border-t border-second/15 px-6 py-4" @submit.prevent="handleSubmit">
      <Input v-model="text" placeholder="Сообщение..." />
      <Button type="submit" :disabled="sending || text.trim() === ''">Отправить</Button>
    </form>
  </div>
</template>
