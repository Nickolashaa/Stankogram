<script setup lang="ts">
import { ref, watch } from "vue"
import Input from "@/components/input.vue"
import Button from "@/components/button.vue"
import { fromDateTimeInput, toDateTimeInput } from "@/lib/format"
import type { SystemNotificationIn } from "@/graphql/base-types"
import type { SystemNotificationFieldsFragment } from "@/graphql/fragments/system-notifications.generated"

const props = defineProps<{
  open: boolean
  title: string
  initialNotification?: SystemNotificationFieldsFragment | null
  submitting?: boolean
}>()

const emit = defineEmits<{
  close: []
  submit: [data: SystemNotificationIn]
}>()

const notificationTitle = ref("")
const text = ref("")
const expiresAt = ref("")

watch(
  () => props.open,
  (isOpen) => {
    if (!isOpen) {
      return
    }
    notificationTitle.value = props.initialNotification?.title ?? ""
    text.value = props.initialNotification?.text ?? ""

    const initialExpiresAt = props.initialNotification?.expiresAt
    expiresAt.value = initialExpiresAt == null ? "" : toDateTimeInput(initialExpiresAt)
  },
  { immediate: true },
)

function handleClose() {
  emit("close")
}

function handleSubmit() {
  if (notificationTitle.value.trim() === "" || text.value.trim() === "") {
    return
  }
  emit("submit", {
    title: notificationTitle.value.trim(),
    text: text.value.trim(),
    expiresAt: expiresAt.value === "" ? null : fromDateTimeInput(expiresAt.value),
  })
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="open"
      class="fixed inset-0 z-50 flex animate-appear items-start justify-center bg-black/45 p-4 backdrop-blur-sm sm:items-center"
      @click.self="handleClose"
    >
      <form
        class="glass-strong hairline shadow-float flex max-h-[calc(100dvh-2rem)] w-full max-w-md animate-pop flex-col gap-4 overflow-y-auto rounded-card p-5 sm:max-h-[85vh] sm:p-8"
        @submit.prevent="handleSubmit"
      >
        <h2 class="m-0 text-xl font-semibold tracking-tight text-main">{{ title }}</h2>

        <Input placeholder="Заголовок" v-model="notificationTitle" />

        <textarea
          v-model="text"
          rows="5"
          placeholder="Текст уведомления"
          class="glass-field hairline box-border w-full resize-y rounded-input px-4 py-3 font-sans text-[15px] text-main outline-none transition-[border-color,box-shadow] duration-200 placeholder:text-second/80 focus-glow"
        />

        <div class="flex flex-col gap-1.5">
          <label class="text-xs font-semibold tracking-wider text-second uppercase">
            Показывать до
          </label>
          <input
            v-model="expiresAt"
            type="datetime-local"
            class="glass-field hairline box-border h-12 w-full rounded-input px-4 font-sans text-[15px] text-main outline-none transition-[border-color,box-shadow] duration-200 focus-glow"
          />
          <span class="text-xs text-second">
            Пустое поле — уведомление висит бессрочно, пока пользователь его не скроет
          </span>
        </div>

        <div class="mt-2 flex gap-2">
          <Button
            type="button"
            variant="ghost"
            class="flex-1"
            icon="cancel"
            :short-mode="false"
            @click="handleClose"
          >
            Отмена
          </Button>
          <Button
            type="submit"
            class="flex-[2]"
            icon="save"
            :short-mode="false"
            :disabled="submitting || notificationTitle.trim() === '' || text.trim() === ''"
          >
            Сохранить
          </Button>
        </div>
      </form>
    </div>
  </Teleport>
</template>
