<script setup lang="ts">
import AdminNav from "@/components/admin-nav.vue"
</script>

<template>
  <div class="flex h-full flex-col lg:flex-row">
    <AdminNav />
    <div class="flex-1 overflow-y-auto px-4 py-6 lg:px-10 lg:py-10">
      <RouterView />
    </div>
  </div>
</template>
