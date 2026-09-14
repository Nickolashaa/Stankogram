const APP_NAME = "Stankogram"
const APP_DESCRIPTION = "мессенджер МГТУ СТАНКИН"
const LOGIN_PATH = "/auth"

export function buildInviteText(email: string, password: string) {
  const url = new URL(LOGIN_PATH, window.location.origin).toString()

  return [
    `Здравствуйте! Для вас создан аккаунт в ${APP_NAME} — ${APP_DESCRIPTION}.`,
    "",
    `Ссылка для входа: ${url}`,
    `Почта: ${email}`,
    `Пароль: ${password}`,
    "",
    "Пароль выдаётся один раз. Если он потеряется, восстановите доступ " +
      "через «Забыли пароль?» на странице входа.",
  ].join("\n")
}
