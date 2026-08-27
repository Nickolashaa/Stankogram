<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import { COLOR_SCHEMES, useThemeStore, type ColorScheme } from "@/stores/theme"
import { notify } from "@/lib/notify"
import Button from "@/components/button.vue"
import NavIcon from "@/components/nav-icon.vue"
import Badge from "@/components/badge.vue"

const props = defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  close: []
}>()

const themeStore = useThemeStore()
const { scheme, isDark } = storeToRefs(themeStore)

const draftScheme = ref<ColorScheme>(scheme.value)
const draftDark = ref(isDark.value)

watch(
  () => props.open,
  (isOpen) => {
    if (!isOpen) {
      return
    }
    draftScheme.value = scheme.value
    draftDark.value = isDark.value
  },
)

function swatchColor(item: (typeof COLOR_SCHEMES)[number], key: "bg" | "accent") {
  return draftDark.value ? item[key].dark : item[key].light
}

function handleClose() {
  emit("close")
}

function handleSave() {
  themeStore.apply(draftScheme.value, draftDark.value)
  notify.success("Тема применена ко всему сайту")
  emit("close")
}

function handleEscape(event: KeyboardEvent) {
  if (event.key === "Escape" && props.open) {
    handleClose()
  }
}

onMounted(() => window.addEventListener("keydown", handleEscape))
onUnmounted(() => window.removeEventListener("keydown", handleEscape))
</script>

<template>
  <div
    v-if="open"
    class="fixed inset-0 z-50 flex animate-appear items-center justify-center bg-black/40 px-4"
    @click.self="handleClose"
  >
    <div
      class="flex h-[92vh] w-full max-w-6xl flex-col overflow-hidden rounded-card bg-card shadow-card lg:flex-row"
    >
      <div
        class="flex min-h-0 w-full flex-1 flex-col border-second/15 lg:w-96 lg:flex-none lg:border-r"
      >
        <div
          class="flex shrink-0 items-center justify-between gap-4 border-b border-second/15 px-4 py-5 lg:px-6"
        >
          <div class="flex flex-col gap-0.5">
            <h2 class="m-0 text-lg font-semibold text-main">Цветовая тема</h2>
            <span class="text-xs text-second">Выберите палитру для всего сайта</span>
          </div>
          <button
            type="button"
            class="cursor-pointer text-second transition-colors duration-150 hover:text-main"
            aria-label="Закрыть"
            @click="handleClose"
          >
            <NavIcon name="cancel" />
          </button>
        </div>

        <div class="mx-4 my-4 flex shrink-0 gap-1 rounded-input bg-second/10 p-1 lg:mx-6">
          <button
            type="button"
            class="flex-1 cursor-pointer rounded-input px-3 py-1.5 text-sm font-medium transition-colors duration-150"
            :class="!draftDark ? 'bg-card text-main shadow-card' : 'text-second hover:text-main'"
            @click="draftDark = false"
          >
            Светлая
          </button>
          <button
            type="button"
            class="flex-1 cursor-pointer rounded-input px-3 py-1.5 text-sm font-medium transition-colors duration-150"
            :class="draftDark ? 'bg-card text-main shadow-card' : 'text-second hover:text-main'"
            @click="draftDark = true"
          >
            Тёмная
          </button>
        </div>

        <div class="flex flex-1 flex-col gap-1.5 overflow-y-auto px-4 pb-4 lg:px-6">
          <button
            v-for="item in COLOR_SCHEMES"
            :key="item.id"
            type="button"
            class="flex cursor-pointer items-center gap-3 rounded-input border-[1.5px] px-3 py-2.5 text-left transition-colors duration-150"
            :class="
              draftScheme === item.id
                ? 'border-accent bg-accent/5'
                : 'border-transparent hover:bg-second/5'
            "
            @click="draftScheme = item.id"
          >
            <span
              class="h-10 w-10 shrink-0 rounded-full shadow-card"
              :style="{
                background: `linear-gradient(135deg, ${swatchColor(item, 'bg')} 50%, ${swatchColor(item, 'accent')} 50%)`,
              }"
            />
            <span class="flex min-w-0 flex-col gap-0.5">
              <span class="text-[15px] font-medium text-main">{{ item.label }}</span>
              <span class="truncate text-xs text-second">{{ item.mood }}</span>
            </span>
            <NavIcon
              v-if="draftScheme === item.id"
              name="save"
              :size="16"
              class="ml-auto shrink-0 text-accent"
            />
          </button>
        </div>

        <div class="flex shrink-0 gap-2 border-t border-second/15 px-4 py-5 lg:px-6">
          <Button
            variant="ghost"
            icon="cancel"
            :short-mode="false"
            class="flex-1"
            @click="handleClose"
          >
            Отмена
          </Button>
          <Button icon="save" :short-mode="false" class="flex-[2]" @click="handleSave">
            Сохранить
          </Button>
        </div>
      </div>

      <div class="hidden flex-1 flex-col bg-second/5 p-6 lg:flex">
        <span class="mb-3 shrink-0 text-xs font-medium tracking-wide text-second uppercase">
          Пример чата
        </span>

        <div
          class="flex flex-1 flex-col overflow-hidden rounded-card shadow-card"
          :class="draftDark ? 'dark' : ''"
          :data-scheme="draftScheme"
        >
          <div class="flex h-full flex-col bg-bg">
            <div
              class="flex shrink-0 items-center gap-3 border-b border-second/15 bg-card px-6 py-5"
            >
              <span
                class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-accent text-[15px] font-semibold text-bg"
              >
                ОР
              </span>
              <div class="flex flex-col">
                <span class="text-[15px] font-semibold text-main">Отдел разработки</span>
                <span class="text-xs text-second">Групповой чат · 5 участников</span>
              </div>
            </div>

            <div class="flex flex-1 flex-col justify-end gap-3 overflow-hidden px-6 py-4">
              <div class="flex flex-col items-start gap-1">
                <div
                  class="max-w-xs rounded-card bg-card px-4 py-2.5 text-[15px] text-main shadow-card"
                >
                  <div
                    class="mb-1 flex flex-wrap items-center gap-1.5 text-xs font-medium opacity-70"
                  >
                    <span>Грачев Николай</span>
                    <Badge variant="role" label="Студент" />
                    <Badge variant="developer" label="Разработчик" />
                  </div>
                  Залил фикс в feature-ветку, нужен ревью до вечера
                </div>
                <span class="px-1 text-xs text-second">14:02</span>
              </div>

              <div class="flex flex-col items-end gap-1 self-end">
                <div class="max-w-xs rounded-card bg-accent px-4 py-2.5 text-[15px] text-bg">
                  Го, гляну как освобожусь
                </div>
                <span class="px-1 text-xs text-second">14:03</span>
              </div>

              <div class="flex flex-col items-start gap-1">
                <div
                  class="max-w-xs rounded-card bg-card px-4 py-2.5 text-[15px] text-main shadow-card"
                >
                  <div
                    class="mb-1 flex flex-wrap items-center gap-1.5 text-xs font-medium opacity-70"
                  >
                    <span>Бердюгин Антон</span>
                    <Badge variant="role" label="Преподаватель" />
                    <Badge variant="chat-admin" label="Админ чата" />
                  </div>
                  API для групповых чатов задеплоили, резолверы уже на проде
                </div>
                <span class="px-1 text-xs text-second">14:05</span>
              </div>

              <div class="flex flex-col items-start gap-1">
                <div
                  class="max-w-xs rounded-card bg-card px-4 py-2.5 text-[15px] text-main shadow-card"
                >
                  <div
                    class="mb-1 flex flex-wrap items-center gap-1.5 text-xs font-medium opacity-70"
                  >
                    <span>Кириллов Фей</span>
                    <Badge variant="role" label="Студент" />
                  </div>
                  Тесты зелёные, мёржу в main
                </div>
                <span class="px-1 text-xs text-second">14:07</span>
              </div>

              <div class="flex flex-col items-start gap-1">
                <div
                  class="max-w-xs rounded-card bg-card px-4 py-2.5 text-[15px] text-main shadow-card"
                >
                  <div
                    class="mb-1 flex flex-wrap items-center gap-1.5 text-xs font-medium opacity-70"
                  >
                    <span>Наточий Влад</span>
                    <Badge variant="role" label="Студент" />
                  </div>
                  Стейджинг живой, логи чистые
                </div>
                <span class="px-1 text-xs text-second">14:09</span>
              </div>

              <div class="flex flex-col items-start gap-1">
                <div
                  class="max-w-xs rounded-card bg-card px-4 py-2.5 text-[15px] text-main shadow-card"
                >
                  <div
                    class="mb-1 flex flex-wrap items-center gap-1.5 text-xs font-medium opacity-70"
                  >
                    <span>Момот Дима</span>
                    <Badge variant="role" label="Студент" />
                  </div>
                  Красота, накатываю на прод
                </div>
                <span class="px-1 text-xs text-second">14:11</span>
              </div>
            </div>

            <div class="flex shrink-0 items-center gap-3 border-t border-second/15 px-6 py-4">
              <div
                class="h-12 flex-1 rounded-input border-[1.5px] border-second/30 bg-bg px-4 py-3 text-[15px] text-second"
              >
                Написать сообщение...
              </div>
              <span
                class="flex h-11 w-11 shrink-0 items-center justify-center rounded-input bg-accent text-bg"
              >
                <NavIcon name="send" :size="18" />
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
