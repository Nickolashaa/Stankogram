import { defineStore } from "pinia"
import { ref, watch } from "vue"
import { apolloClient } from "@/api"
import { LoginDocument } from "@/graphql/mutations/auth/login.generated"
import { RefreshDocument } from "@/graphql/mutations/auth/refresh.generated"
import { LogoutDocument } from "@/graphql/mutations/auth/logout.generated"
import { UserResetPasswordRequestDocument } from "@/graphql/mutations/auth/user-reset-password-request.generated"
import { UserResetPasswordConfirmDocument } from "@/graphql/mutations/auth/user-reset-password-confirm.generated"
import { MeDocument } from "@/graphql/queries/auth/me.generated"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"

const ACCESS_TOKEN_KEY = "accessToken"

export const useAuthStore = defineStore("auth", () => {
  const user = ref<UserFieldsFragment>()
  const accessToken = ref<string | undefined>(localStorage.getItem(ACCESS_TOKEN_KEY) ?? undefined)

  watch(accessToken, (value) => {
    if (value === undefined) {
      localStorage.removeItem(ACCESS_TOKEN_KEY)
    } else {
      localStorage.setItem(ACCESS_TOKEN_KEY, value)
    }
  })

  async function fetchUser() {
    const { data } = await apolloClient.query({
      query: MeDocument,
      fetchPolicy: "network-only",
    })
    user.value = data.me.__typename === "User" ? data.me : undefined
  }

  if (accessToken.value !== undefined) {
    fetchUser()
  }

  async function login(email: string, password: string) {
    const { data } = await apolloClient.mutate({
      mutation: LoginDocument,
      variables: { input: { email, password } },
    })

    if (data === undefined || data === null || data.login.__typename !== "JWTs") {
      throw new Error(data?.login.message ?? "Login failed")
    }

    accessToken.value = data.login.accessToken

    await fetchUser()
  }

  async function requestPasswordReset(email: string) {
    const { data } = await apolloClient.mutate({
      mutation: UserResetPasswordRequestDocument,
      variables: { email },
    })

    if (data?.userResetPasswordRequest) {
      throw new Error(data.userResetPasswordRequest.message)
    }
  }

  async function confirmPasswordReset(id: number, code: string) {
    const { data } = await apolloClient.mutate({
      mutation: UserResetPasswordConfirmDocument,
      variables: { id, code },
    })

    if (data?.userResetPasswordConfirm) {
      throw new Error(data.userResetPasswordConfirm.message)
    }
  }

  async function logout() {
    try {
      await apolloClient.mutate({ mutation: LogoutDocument })
    } catch {}
    accessToken.value = undefined
    user.value = undefined
    await apolloClient.clearStore()
  }

  async function refresh() {
    const { data } = await apolloClient.mutate({ mutation: RefreshDocument })

    if (data === undefined || data === null || data.refresh.__typename !== "JWTs") {
      accessToken.value = undefined
      user.value = undefined
      return
    }

    accessToken.value = data.refresh.accessToken
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
