import { EUserRole } from "@/graphql/base-types"
import { roleLabels } from "@/lib/roles"

export type BadgeVariant = "role" | "developer" | "chat-admin" | "muted"

export type Badge = {
  label: string
  variant: BadgeVariant
}

type BadgeUser = {
  role: EUserRole
  isAdmin: boolean
}

type BadgeParticipant = {
  isAdmin: boolean
  isMuted: boolean
}

export function userBadges(user: BadgeUser): Badge[] {
  const badges: Badge[] = [{ label: roleLabels[user.role], variant: "role" }]

  if (user.isAdmin) {
    badges.push({ label: "Разработчик", variant: "developer" })
  }

  return badges
}

export function participantBadges(user: BadgeUser, participant: BadgeParticipant): Badge[] {
  const badges = userBadges(user)

  if (participant.isAdmin) {
    badges.push({ label: "Админ чата", variant: "chat-admin" })
  }

  if (participant.isMuted) {
    badges.push({ label: "Заглушен", variant: "muted" })
  }

  return badges
}
