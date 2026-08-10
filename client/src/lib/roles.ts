import type { components } from "@/api/schema"

export const roleLabels: Record<components["schemas"]["Role"], string> = {
  STUDENT: "Студент",
  TEACHER: "Преподаватель",
}
