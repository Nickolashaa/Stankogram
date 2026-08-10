<script setup lang="ts">
import AppNav from "@/components/app-nav.vue"
</script>

<template>
  <div class="flex min-h-screen">
    <AppNav />
    <div class="flex flex-1 items-center justify-center overflow-y-auto px-10 py-10">
      <RouterView />
    </div>
  </div>
</template>
