import { formatLastOnline } from "@/lib/format"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"

export type UserPresence = Pick<UserFieldsFragment, "isOnline" | "lastOnlineAt">

export function presenceLabel(presence: UserPresence) {
  if (presence.isOnline) {
    return "в сети"
  }

  if (presence.lastOnlineAt === null) {
    return "был давно"
  }

  return `был в сети ${formatLastOnline(presence.lastOnlineAt)}`
}
