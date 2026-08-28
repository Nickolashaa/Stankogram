<script setup lang="ts">
import { computed } from "vue"
import { useRoute } from "vue-router"
import AppNav from "@/components/app-nav.vue"

const route = useRoute()
const isChatsRoute = computed(() => route.path.startsWith("/chats"))
</script>

<template>
  <div class="flex h-dvh">
    <AppNav />
    <div class="flex-1 overflow-y-auto" :class="isChatsRoute ? '' : 'pb-16 lg:pb-0'">
      <RouterView />
    </div>
  </div>
</template>
