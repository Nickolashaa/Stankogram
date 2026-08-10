<script setup lang="ts">
import { Toaster } from "vue-sonner"
import "vue-sonner/style.css"
import ThemeToggle from "@/components/theme-toggle.vue"
</script>

<template>
  <RouterView />
  <ThemeToggle />
  <Toaster position="top-center" />
</template>
<style scoped></style>
