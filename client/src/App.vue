<script setup lang="ts">
import { onMounted } from "vue";
import { client } from "./api";

onMounted(async () => {
  const { data, error } = await client.GET("/api/health");
})
</script>

<template>
  <h1>Stankogram</h1>
  {{ data }}
  {{ error }}
</template>

<style scoped></style>
