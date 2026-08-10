<script setup lang="ts">
import AppNav from "@/components/app-nav.vue"
</script>

<template>
  <div class="flex min-h-screen">
    <AppNav />
    <div class="flex-1 overflow-y-auto">
      <RouterView />
    </div>
  </div>
</template>
