import { defineStore } from "pinia"
import { ref } from "vue"
import { apolloClient } from "@/api"
import { mutateWithFile } from "@/api/upload"
import { UserCreateDocument } from "@/graphql/mutations/auth/user-create.generated"
import { UserUpdateDocument } from "@/graphql/mutations/auth/user-update.generated"
import { UserDeleteDocument } from "@/graphql/mutations/auth/user-delete.generated"
import { UsersDocument } from "@/graphql/queries/auth/users.generated"
import {
  UsersImportDocument,
  type UsersImportMutation,
} from "@/graphql/mutations/auth/users-import.generated"
import { UsersImportTemplateDocument } from "@/graphql/queries/auth/users-import-template.generated"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import type { UserFiltersIn, UserIn } from "@/graphql/base-types"

export const useUserStore = defineStore("users", () => {
  const users = ref<UserFieldsFragment[]>([])
  const totalCount = ref(0)

  async function fetchUsers(
    filters: UserFiltersIn,
    limit: number,
    offset: number,
    options: { append?: boolean } = {},
  ) {
    const { data } = await apolloClient.query({
      query: UsersDocument,
      variables: { filters, pagination: { limit, offset } },
      fetchPolicy: "network-only",
    })

    users.value = options.append ? [...users.value, ...data.users.users] : data.users.users
    totalCount.value = data.users.count
  }

  async function createUser(input: UserIn) {
    const { data } = await apolloClient.mutate({
      mutation: UserCreateDocument,
      variables: { input },
    })

    if (data === undefined || data === null || data.userCreate.__typename !== "CreatedUser") {
      throw new Error(data?.userCreate.message ?? "Failed to create user")
    }

    return data.userCreate
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

  async function fetchImportTemplate() {
    const { data } = await apolloClient.query({
      query: UsersImportTemplateDocument,
      fetchPolicy: "network-only",
    })

    return data.usersImportTemplate
  }

  async function importUsers(file: File) {
    const data = await mutateWithFile<UsersImportMutation>(UsersImportDocument, file)

    if (data.usersImport.__typename !== "UsersImportReport") {
      throw new Error(data.usersImport.message)
    }

    return data.usersImport
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
    fetchImportTemplate,
    importUsers,
  }
})
