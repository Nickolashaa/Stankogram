<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import { useInfiniteScroll } from "@vueuse/core"
import { useUserStore } from "@/stores/users"
import { fullName } from "@/lib/format"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import type { EUserRole, UserIn } from "@/graphql/base-types"
import Button from "@/components/button.vue"
import AdminUserFilters from "@/components/admin-user-filters.vue"
import AdminUsersTable from "@/components/admin-users-table.vue"
import AdminUserFormDialog from "@/components/admin-user-form-dialog.vue"
import AdminUsersImport from "@/components/admin-users-import.vue"
import UserCredentialsDialog from "@/components/user-credentials-dialog.vue"
import { notify } from "@/lib/notify"

const PAGE_SIZE = 20

const userStore = useUserStore()
const { users, totalCount } = storeToRefs(userStore)

const searchQuery = ref("")
const roleFilter = ref<"" | EUserRole>("")
const isAdminFilter = ref<"" | "true" | "false">("")

const loading = ref(false)

const filterQuery = computed(() => ({
  searchQuery: searchQuery.value.trim() === "" ? undefined : searchQuery.value.trim(),
  role: roleFilter.value === "" ? undefined : roleFilter.value,
  isAdmin: isAdminFilter.value === "" ? undefined : isAdminFilter.value === "true",
}))

async function fetchUsers() {
  loading.value = true
  try {
    await userStore.fetchUsers(filterQuery.value, PAGE_SIZE, 0)
  } finally {
    loading.value = false
  }
}

const infiniteScroll = useInfiniteScroll(
  window,
  async () => {
    await userStore.fetchUsers(filterQuery.value, PAGE_SIZE, users.value.length, {
      append: true,
    })
  },
  {
    distance: 200,
    canLoadMore: () => !loading.value && users.value.length < totalCount.value,
  },
)

watch(filterQuery, () => {
  fetchUsers()
  infiniteScroll.reset()
})

onMounted(fetchUsers)

const credentials = ref<{ email: string; password: string } | null>(null)

const dialogOpen = ref(false)
const dialogMode = ref<"create" | "edit">("create")
const editingUser = ref<UserFieldsFragment | null>(null)
const saving = ref(false)

function openCreateDialog() {
  dialogMode.value = "create"
  editingUser.value = null
  dialogOpen.value = true
}

function openEditDialog(user: UserFieldsFragment) {
  dialogMode.value = "edit"
  editingUser.value = user
  dialogOpen.value = true
}

function closeDialog() {
  dialogOpen.value = false
}

async function handleSubmit(data: UserIn) {
  saving.value = true
  try {
    if (dialogMode.value === "create") {
      const created = await userStore.createUser(data)
      credentials.value = { email: created.user.email, password: created.password }
    } else if (editingUser.value !== null) {
      await userStore.updateUser(editingUser.value.id, data)
      notify.success("Данные пользователя обновлены")
    }
  } catch {
    notify.error("Не удалось сохранить пользователя. Проверьте данные и попробуйте ещё раз")
    return
  } finally {
    saving.value = false
  }

  dialogOpen.value = false
  await fetchUsers()
  infiniteScroll.reset()
}

async function handleImported() {
  await fetchUsers()
  infiniteScroll.reset()
}

async function handleDelete(user: UserFieldsFragment) {
  if (!window.confirm(`Удалить пользователя ${fullName(user)}?`)) {
    return
  }

  try {
    await userStore.deleteUser(user.id)
  } catch {
    notify.error("Не удалось удалить пользователя")
    return
  }

  notify.success("Пользователь удалён")
  await fetchUsers()
  infiniteScroll.reset()
}
</script>

<template>
  <div class="flex animate-appear flex-col gap-6">
    <div class="flex flex-col items-start gap-3 sm:flex-row sm:items-center sm:justify-between">
      <h1 class="m-0 text-2xl font-semibold tracking-tight text-main sm:text-3xl">Пользователи</h1>
      <div class="flex w-full flex-col gap-2 sm:w-auto sm:flex-row sm:items-center">
        <AdminUsersImport @imported="handleImported" />
        <Button icon="plus" :short-mode="false" class="w-full sm:w-auto" @click="openCreateDialog"
          >Создать пользователя</Button
        >
      </div>
    </div>

    <AdminUserFilters
      v-model:search="searchQuery"
      v-model:role="roleFilter"
      v-model:is-admin="isAdminFilter"
    />

    <AdminUsersTable :users="users" @edit="openEditDialog" @delete="handleDelete" />

    <div class="flex items-center justify-between text-sm text-second">
      <span>Всего: {{ totalCount }}</span>
      <span v-if="infiniteScroll.isLoading.value">Загрузка...</span>
    </div>

    <UserCredentialsDialog
      :open="credentials !== null"
      :email="credentials?.email ?? ''"
      :password="credentials?.password ?? ''"
      @close="credentials = null"
    />

    <AdminUserFormDialog
      :open="dialogOpen"
      :title="dialogMode === 'create' ? 'Новый пользователь' : 'Редактирование пользователя'"
      :initial-user="editingUser"
      :submitting="saving"
      @close="closeDialog"
      @submit="handleSubmit"
    />
  </div>
</template>
