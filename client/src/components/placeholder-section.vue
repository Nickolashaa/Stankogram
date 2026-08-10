<script setup lang="ts">
defineProps<{
  title: string
}>()
</script>

<template>
  <div
    class="flex h-full min-h-[60vh] animate-appear flex-col items-center justify-center gap-2 p-10 text-center"
  >
    <h1 class="m-0 text-2xl font-semibold text-main">{{ title }}</h1>
    <p class="m-0 text-second">Раздел в разработке</p>
  </div>
</template>
