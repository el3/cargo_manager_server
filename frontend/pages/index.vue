<script setup lang="ts">
  const { data, error, execute, pending, status } = await useLazyFetch(
    '/api/pallets',
    { query: { trip: 1 }, immediate: true },
  );
</script>

<template>
  <div v-if="status === 'idle'">
    <button @click="execute">Get data.</button>
  </div>

  <div v-else-if="pending">
    Loading comments...
  </div>

  <div v-else>
    <UTable :rows="data.pallets" />
  </div>
</template>
