<script setup lang="ts">
const navItems = [{ to: "/admin/users", label: "Пользователи" }]
</script>

<template>
  <nav class="flex w-56 shrink-0 flex-col gap-1 border-r border-second/15 bg-card px-4 py-8">
    <RouterLink
      v-for="item in navItems"
      :key="item.to"
      :to="item.to"
      class="rounded-input px-4 py-2.5 text-[15px] font-medium text-second transition-colors duration-150 hover:bg-accent/10 hover:text-main"
      active-class="bg-accent/10 text-accent"
    >
      {{ item.label }}
    </RouterLink>
  </nav>
</template>
