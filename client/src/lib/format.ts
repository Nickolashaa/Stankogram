export function fullName(user: { surname: string; name: string; patronymic?: string | null }) {
  return [user.surname, user.name, user.patronymic].filter(Boolean).join(" ")
}

export function shortName(user: { surname: string; name: string }) {
  return `${user.surname} ${user.name}`
}

export function initials(user: { surname: string; name: string }) {
  return `${user.surname[0] ?? ""}${user.name[0] ?? ""}`.toUpperCase()
}

export function chatInitials(title: string) {
  const words = title.trim().split(/\s+/).filter(Boolean)
  if (words.length === 0) {
    return "?"
  }
  if (words.length === 1) {
    return words[0]!.slice(0, 2).toUpperCase()
  }
  return `${words[0]![0]}${words[1]![0]}`.toUpperCase()
}

export function formatDateTime(value: string) {
  return new Date(value).toLocaleString("ru-RU", {
    dateStyle: "short",
    timeStyle: "short",
  })
}

export function formatTime(value: string) {
  return new Date(value).toLocaleTimeString("ru-RU", {
    hour: "2-digit",
    minute: "2-digit",
  })
}

export function formatFullDate(value: Date) {
  const formatted = value.toLocaleDateString("ru-RU", {
    weekday: "long",
    day: "numeric",
    month: "long",
  })
  return formatted.charAt(0).toUpperCase() + formatted.slice(1)
}
