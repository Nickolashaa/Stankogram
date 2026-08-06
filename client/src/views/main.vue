<script setup lang="ts">
import { onMounted, ref } from "vue"
import { storeToRefs } from "pinia"
import { useRouter } from "vue-router"
import { client } from "./../api"
import type { components } from "./../api/schema"
import { useAuthStore } from "@/stores/auth"

const data_var = ref<components["schemas"]["HealthResponse"]>()

onMounted(async () => {
  const { data } = await client.GET("/api/health")
  data_var.value = data
})

const router = useRouter()
const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

async function handleLogout() {
  await authStore.logout()
  router.push("/auth")
}
</script>

<template>
  <template v-if="data_var === undefined"> Loading... </template>
  <template v-else>
    <h1>Stankogram</h1>
    <h2>Code: {{ data_var?.code }}</h2>
    <h3>Message: {{ data_var?.message }}</h3>
    <div class="">
      {{ user ? user : 123 }}
    </div>
    <button @click="handleLogout">Выйти</button>
  </template>
</template>
<style scoped></style>
