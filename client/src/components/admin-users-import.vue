<script setup lang="ts">
import { ref } from "vue"
import Button from "@/components/button.vue"
import { useUserStore } from "@/stores/users"
import { downloadXlsx } from "@/lib/download"
import { notify } from "@/lib/notify"

const emit = defineEmits<{
  imported: []
}>()

const userStore = useUserStore()

const fileInput = ref<HTMLInputElement | null>(null)
const downloading = ref(false)
const importing = ref(false)

async function downloadTemplate() {
  downloading.value = true
  try {
    const template = await userStore.fetchImportTemplate()
    downloadXlsx(template.filename, template.content)
  } catch {
    notify.error("Не удалось скачать шаблон")
  } finally {
    downloading.value = false
  }
}

async function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ""

  if (file === undefined) {
    return
  }

  importing.value = true
  try {
    const report = await userStore.importUsers(file)
    downloadXlsx(report.file.filename, report.file.content)

    if (report.failed === 0) {
      notify.success(
        `Зарегистрировано сотрудников: ${report.succeeded}. Пароли — в скачанном файле`,
      )
    } else {
      notify.warning(
        `Зарегистрировано ${report.succeeded} из ${report.total}, с ошибками: ${report.failed}. ` +
          "Пароли и причины — в скачанном файле",
      )
    }

    emit("imported")
  } catch (error) {
    notify.error(error instanceof Error ? error.message : "Не удалось импортировать сотрудников")
  } finally {
    importing.value = false
  }
}
</script>

<template>
  <div class="flex w-full gap-2 sm:w-auto">
    <input ref="fileInput" type="file" accept=".xlsx" class="hidden" @change="handleFileChange" />

    <Button
      variant="ghost"
      icon="download"
      :short-mode="false"
      :disabled="downloading"
      class="flex-1 sm:flex-none"
      @click="downloadTemplate"
    >
      Шаблон
    </Button>

    <Button
      variant="soft"
      icon="upload"
      :short-mode="false"
      :disabled="importing"
      class="flex-1 sm:flex-none"
      @click="fileInput?.click()"
    >
      {{ importing ? "Импорт..." : "Импорт" }}
    </Button>
  </div>
</template>
