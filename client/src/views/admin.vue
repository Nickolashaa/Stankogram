<script setup lang="ts">
import AdminNav from "@/components/admin-nav.vue"
</script>

<template>
  <div class="flex h-full">
    <AdminNav />
    <div class="flex-1 overflow-y-auto px-10 py-10">
      <RouterView />
    </div>
  </div>
</template>
