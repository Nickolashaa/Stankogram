<script setup lang="ts">
import { watch } from "vue"
import { storeToRefs } from "pinia"
import { Toaster } from "vue-sonner"
import "vue-sonner/style.css"
import { useAuthStore } from "@/stores/auth"
import { router, PUBLIC_PATHS } from "@/router"

const authStore = useAuthStore()
const { accessToken } = storeToRefs(authStore)

watch(accessToken, (value) => {
  if (value === undefined && !PUBLIC_PATHS.includes(router.currentRoute.value.path)) {
    router.push("/auth")
  }
})
</script>

<template>
  <RouterView />
  <Toaster position="top-center" />
</template>
<style scoped></style>
