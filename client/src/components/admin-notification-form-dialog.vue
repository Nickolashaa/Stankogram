<script setup lang="ts">
import { ref, watch } from "vue"
import Input from "@/components/input.vue"
import Button from "@/components/button.vue"
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

watch(
  () => props.open,
  (isOpen) => {
    if (!isOpen) {
      return
    }
    notificationTitle.value = props.initialNotification?.title ?? ""
    text.value = props.initialNotification?.text ?? ""
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
  emit("submit", { title: notificationTitle.value.trim(), text: text.value.trim() })
}
</script>

<template>
  <div
    v-if="open"
    class="fixed inset-0 z-50 flex animate-appear items-center justify-center bg-black/40 px-4"
    @click.self="handleClose"
  >
    <form
      class="flex max-h-[85vh] w-full max-w-md flex-col gap-4 overflow-y-auto rounded-card bg-card p-5 shadow-card sm:p-8"
      @submit.prevent="handleSubmit"
    >
      <h2 class="m-0 text-xl font-semibold text-main">{{ title }}</h2>

      <Input placeholder="Заголовок" v-model="notificationTitle" />

      <textarea
        v-model="text"
        rows="5"
        placeholder="Текст уведомления"
        class="box-border w-full resize-y rounded-input border-[1.5px] border-second/30 bg-bg px-4 py-3 font-sans text-[15px] text-main outline-none transition-colors duration-150 placeholder:text-second focus:border-accent"
      />

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
</template>
