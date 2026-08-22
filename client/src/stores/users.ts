import { defineStore } from "pinia"
import { ref } from "vue"
import { apolloClient } from "@/api"
import { UserCreateDocument } from "@/graphql/mutations/auth/user-create.generated"
import { UserUpdateDocument } from "@/graphql/mutations/auth/user-update.generated"
import { UserDeleteDocument } from "@/graphql/mutations/auth/user-delete.generated"
import { UsersDocument } from "@/graphql/queries/auth/users.generated"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import type { UserFiltersIn, UserIn } from "@/graphql/base-types"

export const useUserStore = defineStore("users", () => {
  const users = ref<UserFieldsFragment[]>([])
  const totalCount = ref(0)

  async function fetchUsers(filters: UserFiltersIn, limit: number, offset: number) {
    const { data } = await apolloClient.query({
      query: UsersDocument,
      variables: { filters, pagination: { limit, offset } },
      fetchPolicy: "network-only",
    })

    users.value = data.users.users
    totalCount.value = data.users.count
  }

  async function createUser(input: UserIn) {
    const { data } = await apolloClient.mutate({
      mutation: UserCreateDocument,
      variables: { input },
    })

    if (data === undefined || data === null || data.userCreate.__typename !== "User") {
      throw new Error(data?.userCreate.message ?? "Failed to create user")
    }
  }

  async function updateUser(id: number, input: UserIn) {
    const { data } = await apolloClient.mutate({
      mutation: UserUpdateDocument,
      variables: { id, input },
    })

    if (data === undefined || data === null || data.userUpdate.__typename !== "User") {
      throw new Error(data?.userUpdate.message ?? "Failed to update user")
    }
  }

  async function deleteUser(id: number) {
    await apolloClient.mutate({
      mutation: UserDeleteDocument,
      variables: { id },
    })
  }

  return {
    users,
    totalCount,
    fetchUsers,
    createUser,
    updateUser,
    deleteUser,
  }
})
