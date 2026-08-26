export function fullName(user: { surname: string; name: string; patronymic?: string | null }) {
  return [user.surname, user.name, user.patronymic].filter(Boolean).join(" ")
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
