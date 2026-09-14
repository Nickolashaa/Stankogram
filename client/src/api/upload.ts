import { print, type DocumentNode } from "graphql"
import { API_URL, UNAUTHORIZED_MESSAGES } from "@/api"
import { useAuthStore } from "@/stores/auth"

type GraphQLResponse<TData> = {
  data?: TData
  errors?: { message: string }[]
}

function buildBody(document: DocumentNode, file: File, variables: Record<string, unknown>) {
  const body = new FormData()
  body.append(
    "operations",
    JSON.stringify({ query: print(document), variables: { ...variables, file: null } }),
  )
  body.append("map", JSON.stringify({ "0": ["variables.file"] }))
  body.append("0", file)
  return body
}

async function send<TData>(
  document: DocumentNode,
  file: File,
  variables: Record<string, unknown>,
  accessToken: string | undefined,
): Promise<GraphQLResponse<TData>> {
  const response = await fetch(API_URL, {
    method: "POST",
    credentials: "include",
    headers: accessToken !== undefined ? { Authorization: `Bearer ${accessToken}` } : {},
    body: buildBody(document, file, variables),
  })

  return (await response.json()) as GraphQLResponse<TData>
}

export async function mutateWithFile<TData>(
  document: DocumentNode,
  file: File,
  variables: Record<string, unknown> = {},
): Promise<TData> {
  const authStore = useAuthStore()

  let result = await send<TData>(document, file, variables, authStore.accessToken)

  if (result.errors?.some((error) => UNAUTHORIZED_MESSAGES.has(error.message)) === true) {
    await authStore.refresh()
    result = await send<TData>(document, file, variables, authStore.accessToken)
  }

  if (result.data === undefined || result.errors !== undefined) {
    throw new Error(result.errors?.[0]?.message ?? "Не удалось загрузить файл")
  }

  return result.data
}
