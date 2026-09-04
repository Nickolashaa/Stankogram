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

export function isSameDay(first: string, second: string) {
  const a = new Date(first)
  const b = new Date(second)
  return (
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate()
  )
}

export function formatDaySeparator(value: string) {
  const date = new Date(value)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(today.getDate() - 1)

  if (isSameDay(value, today.toISOString())) {
    return "Сегодня"
  }

  if (isSameDay(value, yesterday.toISOString())) {
    return "Вчера"
  }

  const formatted = date.toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    ...(date.getFullYear() === today.getFullYear() ? {} : { year: "numeric" }),
  })

  return formatted.charAt(0).toUpperCase() + formatted.slice(1)
}
