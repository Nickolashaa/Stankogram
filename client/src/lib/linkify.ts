export type TextSegment = { type: "text"; value: string }
export type LinkSegment = { type: "link"; value: string; href: string }
export type MessageSegment = TextSegment | LinkSegment

export const LINK_TOP_LEVEL_DOMAINS = [
  "ru",
  "рф",
  "su",
  "com",
  "net",
  "org",
  "info",
  "biz",
  "pro",
  "name",
  "online",
  "site",
  "space",
  "store",
  "shop",
  "tech",
  "website",
  "xyz",
  "top",
  "dev",
  "app",
  "io",
  "ai",
  "me",
  "tv",
  "cc",
  "edu",
  "gov",
  "int",
  "by",
  "kz",
  "ua",
  "uz",
  "kg",
  "am",
  "az",
  "ge",
  "tj",
  "tm",
  "at",
  "ch",
  "cz",
  "de",
  "dk",
  "es",
  "fi",
  "fr",
  "it",
  "nl",
  "no",
  "pt",
  "se",
  "eu",
  "uk",
  "us",
  "ca",
  "au",
  "br",
  "cn",
  "in",
  "il",
  "jp",
  "kr",
  "tr",
]

const DOMAIN_LABEL = "[a-zа-яё0-9](?:[a-zа-яё0-9-]*[a-zа-яё0-9])?"
const BARE_DOMAIN =
  `(?<![@\\w.\\-а-яё])(?:${DOMAIN_LABEL}\\.)+(?:${LINK_TOP_LEVEL_DOMAINS.join("|")})` +
  `(?![a-zа-яё0-9\\-_])(?::\\d{1,5})?(?:[/?#][^\\s<>"']*)?`

const LINK_PATTERN = new RegExp(`(?:https?://|www\\.)[^\\s<>"']+|${BARE_DOMAIN}`, "gi")
const TRAILING_PUNCTUATION = /[.,!?;:»)\]}'"]+$/

function splitTrailing(match: string) {
  let value = match
  let trailing = ""

  const punctuation = value.match(TRAILING_PUNCTUATION)
  if (punctuation) {
    trailing = punctuation[0]
    value = value.slice(0, value.length - trailing.length)
  }

  while (trailing.startsWith(")")) {
    const openCount = (value.match(/\(/g) ?? []).length
    const closeCount = (value.match(/\)/g) ?? []).length
    if (openCount <= closeCount) {
      break
    }
    value += ")"
    trailing = trailing.slice(1)
  }

  return { value, trailing }
}

export function linkify(text: string): MessageSegment[] {
  const segments: MessageSegment[] = []
  let lastIndex = 0

  for (const match of text.matchAll(LINK_PATTERN)) {
    const raw = match[0]
    const start = match.index

    const { value, trailing } = splitTrailing(raw)
    if (value === "" || /^https?:\/\/$/i.test(value)) {
      continue
    }

    if (start > lastIndex) {
      segments.push({ type: "text", value: text.slice(lastIndex, start) })
    }

    segments.push({
      type: "link",
      value,
      href: /^https?:\/\//i.test(value) ? value : `https://${value}`,
    })

    if (trailing !== "") {
      segments.push({ type: "text", value: trailing })
    }

    lastIndex = start + raw.length
  }

  if (lastIndex < text.length) {
    segments.push({ type: "text", value: text.slice(lastIndex) })
  }

  return segments
}
