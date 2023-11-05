<script setup lang="ts">
  const { data, error, execute, pending, status } = await useLazyFetch('http://0.0.0.0:8080/api/pallets?trip=1')
</script>

<template>
  <div v-if="status === 'idle'">
    <button @click="execute">Get data</button>
  </div>

  <div v-else-if="pending">
    Loading comments...
  </div>

  <div v-else>
    {{ data }}
     <!-- <UTable :rows="data.pallets" /> -->
  </div>
</template>
