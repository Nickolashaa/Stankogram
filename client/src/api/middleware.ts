import type { Middleware } from "openapi-fetch"
import { useAuthStore } from "../stores/auth"

export const AuthMiddleware: Middleware = {
  async onRequest({ request }) {
    const { accessToken } = useAuthStore()
    if (accessToken !== undefined) {
      request.headers.set("Authorization", `Bearer ${accessToken}`)
    }
    return request
  },

  async onResponse({ request, response }) {
    if (response.status !== 401 || request.url.endsWith("/api/auth/refresh")) {
      return response
    }

    const auth = useAuthStore()
    try {
      await auth.refresh()
    } catch {
      return response
    }

    const retryRequest = request.clone()
    retryRequest.headers.set("Authorization", `Bearer ${auth.accessToken}`)
    return fetch(retryRequest)
  },
}
