<script setup lang="ts">
defineProps<{
  title: string
}>()
</script>

<template>
  <div
    class="flex min-h-full animate-rise flex-col items-center justify-center gap-2 p-6 text-center sm:p-10"
  >
    <div
      class="glass hairline shadow-card flex flex-col items-center gap-3 rounded-card px-10 py-12"
    >
      <h1 class="gradient-text m-0 text-2xl font-semibold tracking-tight">
        {{ title }}
      </h1>
      <p class="m-0 text-second">Раздел в разработке</p>
    </div>
  </div>
</template>
