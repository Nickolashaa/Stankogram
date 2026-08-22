import { EUserRole } from "@/graphql/base-types"

export const roleLabels: Record<EUserRole, string> = {
  [EUserRole.Student]: "Студент",
  [EUserRole.Teacher]: "Преподаватель",
}
