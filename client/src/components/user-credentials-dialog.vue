<script setup lang="ts">
import { useClipboard } from "@vueuse/core"
import Button from "@/components/button.vue"
import { notify } from "@/lib/notify"

const props = defineProps<{
  open: boolean
  email: string
  password: string
}>()

const emit = defineEmits<{
  close: []
}>()

const { copy, isSupported } = useClipboard()

async function copyCredentials() {
  await copy(`${props.email}\n${props.password}`)
  notify.success("Данные для входа скопированы")
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="open"
      class="fixed inset-0 z-50 flex animate-appear items-start justify-center bg-black/45 p-4 backdrop-blur-sm sm:items-center"
      @click.self="emit('close')"
    >
      <div
        class="glass-strong hairline shadow-float flex w-full max-w-md animate-pop flex-col gap-4 rounded-card p-5 sm:p-8"
      >
        <h2 class="m-0 text-xl font-semibold tracking-tight text-main">Пользователь создан</h2>

        <p class="m-0 text-sm text-second">
          Пароль показывается один раз — передайте данные сотруднику. Забытый пароль
          восстанавливается через «Забыли пароль?» на странице входа.
        </p>

        <div class="glass-field hairline flex flex-col gap-3 rounded-input px-4 py-3">
          <div class="flex flex-col gap-1">
            <span class="text-xs font-semibold tracking-wider text-second uppercase">Почта</span>
            <span class="font-mono text-[15px] break-all text-main">{{ email }}</span>
          </div>
          <div class="flex flex-col gap-1">
            <span class="text-xs font-semibold tracking-wider text-second uppercase">Пароль</span>
            <span class="font-mono text-[15px] break-all text-main">{{ password }}</span>
          </div>
        </div>

        <div class="mt-2 flex gap-2">
          <Button
            v-if="isSupported"
            variant="soft"
            icon="save"
            :short-mode="false"
            class="flex-1"
            @click="copyCredentials"
          >
            Скопировать
          </Button>
          <Button icon="cancel" :short-mode="false" class="flex-1" @click="emit('close')">
            Готово
          </Button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
