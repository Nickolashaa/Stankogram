import { defineStore } from "pinia"
import { ref, watch } from "vue"
import { client } from "./../api"
import type { components } from "./../api/schema"

const ACCESS_TOKEN_KEY = "accessToken"

export const useAuthStore = defineStore("auth", () => {
  const user = ref<components["schemas"]["UserResponse"]>()
  const accessToken = ref<string | undefined>(localStorage.getItem(ACCESS_TOKEN_KEY) ?? undefined)

  watch(accessToken, (value) => {
    if (value === undefined) {
      localStorage.removeItem(ACCESS_TOKEN_KEY)
    } else {
      localStorage.setItem(ACCESS_TOKEN_KEY, value)
    }
  })

  async function fetchUser() {
    const { data } = await client.GET("/api/auth/me")
    user.value = data
  }

  if (accessToken.value !== undefined) {
    fetchUser()
  }

  async function login(email: string, password: string) {
    const { data, error } = await client.POST("/api/auth/login", {
      body: { email, password },
    })

    if (error !== undefined) {
      throw new Error(error.detail?.toString())
    }

    accessToken.value = data.access_token

    await fetchUser()
  }

  async function requestPasswordReset(email: string) {
    const { error } = await client.POST("/api/auth/reset_password_request", {
      body: { email },
    })

    if (error !== undefined) {
      throw new Error(error.detail?.toString())
    }
  }

  async function confirmPasswordReset(id: number, code: string) {
    const { error } = await client.POST("/api/auth/reset_password_confirm", {
      body: { id, code },
    })

    if (error !== undefined) {
      throw new Error(error.detail?.toString())
    }
  }

  async function logout() {
    await client.POST("/api/auth/logout")
    accessToken.value = undefined
    user.value = undefined
  }

  async function refresh() {
    const { data, error } = await client.POST("/api/auth/refresh")

    if (error !== undefined) {
      accessToken.value = undefined
      user.value = undefined
      return
    }

    accessToken.value = data.access_token
  }

  return {
    login,
    logout,
    requestPasswordReset,
    confirmPasswordReset,
    user,
    accessToken,
    refresh,
  }
})
