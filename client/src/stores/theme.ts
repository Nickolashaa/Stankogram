import { defineStore } from "pinia"
import { ref, watch } from "vue"

const THEME_KEY = "theme"

type Theme = "light" | "dark"

function getInitialTheme(): Theme {
  const stored = localStorage.getItem(THEME_KEY)
  if (stored === "light" || stored === "dark") {
    return stored
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
}

export const useThemeStore = defineStore("theme", () => {
  const theme = ref<Theme>(getInitialTheme())

  watch(
    theme,
    (value) => {
      document.documentElement.classList.toggle("dark", value === "dark")
      localStorage.setItem(THEME_KEY, value)
    },
    { immediate: true },
  )

  function toggle() {
    theme.value = theme.value === "dark" ? "light" : "dark"
  }

  return { theme, toggle }
})
