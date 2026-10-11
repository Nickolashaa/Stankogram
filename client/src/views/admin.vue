<script setup lang="ts">
import AdminNav from "@/components/admin-nav.vue"
</script>

<template>
  <div class="flex h-full flex-col lg:flex-row">
    <AdminNav />
    <div class="min-h-0 flex-1">
      <RouterView />
    </div>
  </div>
</template>
