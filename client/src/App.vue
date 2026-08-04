<script setup lang="ts">
import { onMounted, ref } from "vue";
import { client } from "./api";
import type { components } from "./api/schema";

const data_var = ref<components["schemas"]["HealthResponse"]>();

onMounted(async () => {
  const { data } = await client.GET("/api/health");
  data_var.value = data;
})
</script>

<template>
  <template v-if="data_var === undefined"">Loading...</template>
  <template v-else>
    <h1>Stankogram</h1>
    <h2>Code: {{ data_var?.code }}</h2>
    <h3>Message: {{ data_var?.message }}</h3>
  </template>
</template>
<style scoped></style>
