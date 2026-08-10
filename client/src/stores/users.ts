import { defineStore } from "pinia"
import { ref } from "vue"
import { client } from "./../api"
import type { components, paths } from "./../api/schema"

type UserResponse = components["schemas"]["UserResponse"]
type UserInput = components["schemas"]["UserInput"]
type UserFilters = NonNullable<paths["/api/users/count"]["get"]["parameters"]["query"]>

export const useUserStore = defineStore("users", () => {
  const users = ref<UserResponse[]>([])
  const totalCount = ref(0)

  async function fetchUsers(filters: UserFilters, limit: number, offset: number) {
    const [{ data: usersData }, { data: countData }] = await Promise.all([
      client.GET("/api/users", {
        params: { query: { ...filters, limit, offset } },
      }),
      client.GET("/api/users/count", { params: { query: filters } }),
    ])

    users.value = usersData ?? []
    totalCount.value = countData ?? 0
  }

  async function createUser(data: UserInput) {
    const { error } = await client.POST("/api/users/create", { body: data })

    if (error !== undefined) {
      throw new Error(error.detail?.toString())
    }
  }

  async function updateUser(id: number, data: UserInput) {
    const { error } = await client.PUT("/api/users/{id}/update", {
      params: { path: { id } },
      body: data,
    })

    if (error !== undefined) {
      throw new Error(error.detail?.toString())
    }
  }

  async function deleteUser(id: number) {
    const { error } = await client.DELETE("/api/users/delete", {
      params: { query: { id } },
    })

    if (error !== undefined) {
      throw new Error(error.detail?.toString())
    }
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
