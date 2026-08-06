import createClient from "openapi-fetch"
import type { paths } from "./schema"
import { AuthMiddleware } from "./middleware"

export const client = createClient<paths>({
  baseUrl: import.meta.env.VITE_API_URL,
  credentials: "include",
})

client.use(AuthMiddleware)
