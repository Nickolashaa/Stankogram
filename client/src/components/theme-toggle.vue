<script setup lang="ts">
import { storeToRefs } from "pinia"
import { computed, onBeforeUnmount, ref } from "vue"
import { type ColorScheme, COLOR_SCHEMES, useThemeStore } from "@/stores/theme"

const themeStore = useThemeStore()
const { theme, scheme } = storeToRefs(themeStore)

const root = ref<HTMLElement | null>(null)
const menuOpen = ref(false)

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

function selectScheme(id: ColorScheme) {
  themeStore.setScheme(id)
  menuOpen.value = false
}

function swatchColor(item: (typeof COLOR_SCHEMES)[number]) {
  return theme.value === "dark" ? item.accent.dark : item.accent.light
}

const currentAccent = computed(() => {
  const active = COLOR_SCHEMES.find((item) => item.id === scheme.value) ?? COLOR_SCHEMES[0]
  return swatchColor(active)
})

function handleOutsideClick(event: MouseEvent) {
  if (menuOpen.value && root.value && !root.value.contains(event.target as Node)) {
    menuOpen.value = false
  }
}

document.addEventListener("click", handleOutsideClick)
onBeforeUnmount(() => document.removeEventListener("click", handleOutsideClick))
</script>

<template>
  <div ref="root" class="group fixed right-6 bottom-6 z-50" @mouseleave="menuOpen = false">
    <div
      class="absolute top-1/2 right-full flex -translate-y-1/2 items-center pr-3 transition-opacity duration-150"
      :class="
        menuOpen
          ? 'pointer-events-auto opacity-100'
          : 'pointer-events-none opacity-0 group-hover:pointer-events-auto group-hover:opacity-100'
      "
    >
      <div
        role="menu"
        class="flex items-center gap-2 rounded-full border border-second/15 bg-card px-3 py-2 shadow-card"
      >
        <button
          v-for="item in COLOR_SCHEMES"
          :key="item.id"
          type="button"
          role="menuitemradio"
          :aria-checked="scheme === item.id"
          :aria-label="item.label"
          :title="item.label"
          class="h-6 w-6 cursor-pointer rounded-full border-2 transition-transform duration-150 hover:scale-110"
          :class="scheme === item.id ? 'border-main' : 'border-transparent'"
          :style="{ backgroundColor: swatchColor(item) }"
          @click="selectScheme(item.id)"
        />
      </div>
    </div>

    <button
      type="button"
      :aria-label="theme === 'dark' ? 'Включить светлую тему' : 'Включить тёмную тему'"
      class="flex h-11 w-11 cursor-pointer items-center justify-center rounded-full border border-second/15 bg-card text-second shadow-card transition-colors duration-150 hover:text-accent"
      @click="themeStore.toggle"
    >
      <svg
        v-if="theme === 'dark'"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="h-5 w-5"
      >
        <circle cx="12" cy="12" r="4" />
        <path
          d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"
        />
      </svg>
      <svg
        v-else
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="h-5 w-5"
      >
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z" />
      </svg>
    </button>

    <button
      type="button"
      aria-label="Цветовые схемы"
      aria-haspopup="true"
      :aria-expanded="menuOpen"
      class="absolute -top-1 -left-1 h-4 w-4 cursor-pointer rounded-full border-2 border-card shadow-card"
      :style="{ backgroundColor: currentAccent }"
      @click.stop="toggleMenu"
    />
  </div>
</template>
