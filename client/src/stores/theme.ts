import { defineStore } from "pinia"
import { watch } from "vue"
import { useDark, useStorage } from "@vueuse/core"

const SCHEME_KEY = "colorScheme"

export const COLOR_SCHEMES = [
  { id: "forest", label: "Лес", accent: { light: "#4f8a76", dark: "#6bb69b" } },
  { id: "ocean", label: "Океан", accent: { light: "#3d7dd8", dark: "#5b9bf0" } },
  { id: "violet", label: "Фиолет", accent: { light: "#7c5cd6", dark: "#9b7ef0" } },
  { id: "sunset", label: "Закат", accent: { light: "#d97a3f", dark: "#f0954f" } },
  { id: "rose", label: "Роза", accent: { light: "#d9456f", dark: "#f06690" } },
] as const

export type ColorScheme = (typeof COLOR_SCHEMES)[number]["id"]

export const useThemeStore = defineStore("theme", () => {
  const isDark = useDark({ storageKey: "theme", initialValue: "light", disableTransition: false })
  const scheme = useStorage<ColorScheme>(SCHEME_KEY, "ocean")

  watch(
    scheme,
    (value) => {
      document.documentElement.dataset.scheme = value
    },
    { immediate: true },
  )

  function toggle() {
    isDark.value = !isDark.value
  }

  function setScheme(next: ColorScheme) {
    scheme.value = next
  }

  return { isDark, scheme, toggle, setScheme }
})
