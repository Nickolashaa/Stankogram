<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import { useUserStore } from "@/stores/users"
import type { UserFieldsFragment } from "@/graphql/fragments/auth.generated"
import type { EUserRole, UserIn } from "@/graphql/base-types"
import Button from "@/components/button.vue"
import AdminUserFilters from "@/components/admin-user-filters.vue"
import AdminUsersTable from "@/components/admin-users-table.vue"
import AdminUserFormDialog from "@/components/admin-user-form-dialog.vue"
import { notify } from "@/lib/notify"

const PAGE_SIZE = 20

const userStore = useUserStore()
const { users, totalCount } = storeToRefs(userStore)

const searchQuery = ref("")
const roleFilter = ref<"" | EUserRole>("")
const isAdminFilter = ref<"" | "true" | "false">("")

const page = ref(1)
const loading = ref(false)

const filterQuery = computed(() => ({
  searchQuery: searchQuery.value.trim() === "" ? undefined : searchQuery.value.trim(),
  role: roleFilter.value === "" ? undefined : roleFilter.value,
  isAdmin: isAdminFilter.value === "" ? undefined : isAdminFilter.value === "true",
}))

const totalPages = computed(() => Math.max(1, Math.ceil(totalCount.value / PAGE_SIZE)))

async function fetchUsers() {
  loading.value = true
  try {
    await userStore.fetchUsers(filterQuery.value, PAGE_SIZE, (page.value - 1) * PAGE_SIZE)
  } finally {
    loading.value = false
  }
}

watch(filterQuery, () => {
  page.value = 1
  fetchUsers()
})

watch(page, fetchUsers)

onMounted(fetchUsers)

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
      await userStore.createUser(data)
      notify.success("Пользователь создан, данные для входа отправлены на почту")
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
}

async function handleDelete(user: UserFieldsFragment) {
  const fullName = [user.surname, user.name].filter(Boolean).join(" ")
  if (!window.confirm(`Удалить пользователя ${fullName}?`)) {
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
}
</script>

<template>
  <div class="flex animate-appear flex-col gap-6">
    <div class="flex items-center justify-between gap-4">
      <h1 class="m-0 text-2xl font-semibold text-main">Пользователи</h1>
      <Button icon="plus" :short-mode="false" @click="openCreateDialog"
        >Создать пользователя</Button
      >
    </div>

    <AdminUserFilters
      v-model:search="searchQuery"
      v-model:role="roleFilter"
      v-model:is-admin="isAdminFilter"
    />

    <AdminUsersTable :users="users" @edit="openEditDialog" @delete="handleDelete" />

    <div class="flex items-center justify-between text-sm text-second">
      <span>Всего: {{ totalCount }}</span>
      <div class="flex items-center gap-3">
        <button
          type="button"
          class="cursor-pointer text-second transition-colors duration-150 hover:text-main disabled:cursor-not-allowed disabled:opacity-40"
          :disabled="page <= 1"
          @click="page -= 1"
        >
          Назад
        </button>
        <span>{{ page }} / {{ totalPages }}</span>
        <button
          type="button"
          class="cursor-pointer text-second transition-colors duration-150 hover:text-main disabled:cursor-not-allowed disabled:opacity-40"
          :disabled="page >= totalPages"
          @click="page += 1"
        >
          Далее
        </button>
      </div>
    </div>

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
