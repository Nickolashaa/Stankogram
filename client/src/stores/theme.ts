import { defineStore } from "pinia"
import { ref, watch } from "vue"

const THEME_KEY = "theme"
const SCHEME_KEY = "colorScheme"

type Theme = "light" | "dark"

export const COLOR_SCHEMES = [
  { id: "forest", label: "Лес", accent: { light: "#4f8a76", dark: "#6bb69b" } },
  { id: "ocean", label: "Океан", accent: { light: "#3d7dd8", dark: "#5b9bf0" } },
  { id: "violet", label: "Фиолет", accent: { light: "#7c5cd6", dark: "#9b7ef0" } },
  { id: "sunset", label: "Закат", accent: { light: "#d97a3f", dark: "#f0954f" } },
  { id: "rose", label: "Роза", accent: { light: "#d9456f", dark: "#f06690" } },
] as const

export type ColorScheme = (typeof COLOR_SCHEMES)[number]["id"]

function getInitialTheme(): Theme {
  const stored = localStorage.getItem(THEME_KEY)
  if (stored === "light" || stored === "dark") {
    return stored
  }

  return "light"
}

function getInitialScheme(): ColorScheme {
  const stored = localStorage.getItem(SCHEME_KEY)
  if (COLOR_SCHEMES.some((item) => item.id === stored)) {
    return stored as ColorScheme
  }

  return "ocean"
}

export const useThemeStore = defineStore("theme", () => {
  const theme = ref<Theme>(getInitialTheme())
  const scheme = ref<ColorScheme>(getInitialScheme())

  watch(
    theme,
    (value) => {
      document.documentElement.classList.toggle("dark", value === "dark")
      localStorage.setItem(THEME_KEY, value)
    },
    { immediate: true },
  )

  watch(
    scheme,
    (value) => {
      document.documentElement.dataset.scheme = value
      localStorage.setItem(SCHEME_KEY, value)
    },
    { immediate: true },
  )

  function toggle() {
    theme.value = theme.value === "dark" ? "light" : "dark"
  }

  function setScheme(next: ColorScheme) {
    scheme.value = next
  }

  return { theme, scheme, toggle, setScheme }
})
