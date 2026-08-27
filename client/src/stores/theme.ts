import { defineStore } from "pinia"
import { watch } from "vue"
import { useDark, useStorage } from "@vueuse/core"

const SCHEME_KEY = "colorScheme"

export const COLOR_SCHEMES = [
  {
    id: "emerald",
    label: "Изумруд",
    mood: "Свежий и уверенный",
    bg: { light: "#f3f6f2", dark: "#0f1713" },
    accent: { light: "#1f8f63", dark: "#4cc794" },
  },
  {
    id: "midnight",
    label: "Полночь",
    mood: "Глубокий и сосредоточенный",
    bg: { light: "#f2f2fa", dark: "#0d0e1a" },
    accent: { light: "#4448c9", dark: "#7478f2" },
  },
  {
    id: "terracotta",
    label: "Терракота",
    mood: "Тёплый и уютный",
    bg: { light: "#faf4ee", dark: "#1c140d" },
    accent: { light: "#b8551f", dark: "#ea8148" },
  },
  {
    id: "coral",
    label: "Коралл",
    mood: "Яркий и энергичный",
    bg: { light: "#f1faf8", dark: "#0d1917" },
    accent: { light: "#d85f45", dark: "#ff8a6b" },
  },
  {
    id: "lavender",
    label: "Лаванда",
    mood: "Мягкий и утончённый",
    bg: { light: "#f7f3fb", dark: "#150f1d" },
    accent: { light: "#7f4fc4", dark: "#ac86e6" },
  },
  {
    id: "graphite",
    label: "Графит",
    mood: "Минимализм и строгость",
    bg: { light: "#f4f4f5", dark: "#0a0a0b" },
    accent: { light: "#2454d6", dark: "#5c8cf0" },
  },
  {
    id: "amber",
    label: "Янтарь",
    mood: "Золотой и гостеприимный",
    bg: { light: "#fbf6ec", dark: "#191307" },
    accent: { light: "#ad7311", dark: "#f0b23f" },
  },
  {
    id: "rose",
    label: "Роза",
    mood: "Насыщенный и элегантный",
    bg: { light: "#fbf1f4", dark: "#1a0e13" },
    accent: { light: "#b82b5d", dark: "#ea6b96" },
  },
  {
    id: "teal",
    label: "Морская волна",
    mood: "Прохладный и глубокий",
    bg: { light: "#eef7f7", dark: "#0a1716" },
    accent: { light: "#12766e", dark: "#35bdb0" },
  },
  {
    id: "turquoise",
    label: "Бирюза",
    mood: "Тропический и живой",
    bg: { light: "#e9fbf7", dark: "#061815" },
    accent: { light: "#049688", dark: "#16d9bd" },
  },
  {
    id: "slate",
    label: "Сланец",
    mood: "Сдержанный и деловой",
    bg: { light: "#f2f4f7", dark: "#10151b" },
    accent: { light: "#45607e", dark: "#6e93b8" },
  },
  {
    id: "plum",
    label: "Слива",
    mood: "Роскошный и таинственный",
    bg: { light: "#f8f2f8", dark: "#180f1a" },
    accent: { light: "#8a3a82", dark: "#c164ba" },
  },
  {
    id: "wine",
    label: "Бордо",
    mood: "Изысканный и терпкий",
    bg: { light: "#f9f1f1", dark: "#1a0d0e" },
    accent: { light: "#7a1f2b", dark: "#c94655" },
  },
  {
    id: "crimson",
    label: "Багрянец",
    mood: "Смелый и страстный",
    bg: { light: "#fdf1f0", dark: "#1c0f0d" },
    accent: { light: "#c62828", dark: "#ef5350" },
  },
  {
    id: "olive",
    label: "Олива",
    mood: "Землистый и спокойный",
    bg: { light: "#f6f6ec", dark: "#16160a" },
    accent: { light: "#6b7024", dark: "#a3ab3f" },
  },
  {
    id: "mustard",
    label: "Горчица",
    mood: "Солнечный и дерзкий",
    bg: { light: "#fbf7e8", dark: "#1a1608" },
    accent: { light: "#9c7615", dark: "#e8b73f" },
  },
  {
    id: "mint",
    label: "Мята",
    mood: "Лёгкий и освежающий",
    bg: { light: "#eefaf3", dark: "#0a1712" },
    accent: { light: "#2fa876", dark: "#4fd39c" },
  },
  {
    id: "peach",
    label: "Персик",
    mood: "Нежный и тёплый",
    bg: { light: "#fdf3ee", dark: "#1c110b" },
    accent: { light: "#d9714a", dark: "#f18e63" },
  },
  {
    id: "copper",
    label: "Медь",
    mood: "Тёплый и металличный",
    bg: { light: "#fbf3ec", dark: "#19110a" },
    accent: { light: "#a85a28", dark: "#d68445" },
  },
  {
    id: "sand",
    label: "Песок",
    mood: "Натуральный и мягкий",
    bg: { light: "#f8f5ee", dark: "#17140f" },
    accent: { light: "#7a6340", dark: "#baa27a" },
  },
] as const

export type ColorScheme = (typeof COLOR_SCHEMES)[number]["id"]

const DEFAULT_SCHEME: ColorScheme = "emerald"

export function getSchemeMeta(id: string) {
  return COLOR_SCHEMES.find((item) => item.id === id) ?? COLOR_SCHEMES[0]
}

export const useThemeStore = defineStore("theme", () => {
  const isDark = useDark({ storageKey: "theme", initialValue: "light", disableTransition: false })
  const scheme = useStorage<ColorScheme>(SCHEME_KEY, DEFAULT_SCHEME)

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

  function apply(next: ColorScheme, dark: boolean) {
    scheme.value = next
    isDark.value = dark
  }

  return { isDark, scheme, toggle, setScheme, apply }
})
