<script setup lang="ts">

const columns = [{
  key: 'id',
  label: 'ID'
}, {
  key: 'datetime',
  label: 'Date'
}, {
  key: 'year',
  label: 'Year'
}, {
  key: 'trip',
  label: 'Trip'
}, {
  key: 'hold',
  label: "Hold"
}, {
  key: 'space',
  label: 'Space'
}, {
  key: 'layer',
  label: 'Layer'
}, {
  key: 'label',
  label: 'Label'
}]

  const years = [2023, 2024];
  const year = ref(years[0]);
  const trips = [1, 2, 3, 4];
  const trip = ref(trips[0]);

// Define the reactive fetch URL
  const fetchUrl = computed(() => `/api/pallets/${year.value}/${trip.value}`);

// Setup the fetch
  const { data, isFetching, error, execute } = useFetch(fetchUrl);

// Watchers to re-fetch data when year or trip changes
  watch([year, trip], () => {
    execute();
  }, { immediate: true });

</script>

<template>
  <div v-if="status === 'idle'">
    <button @click="execute">Get data.</button>
  </div>

  <div v-else-if="pending">
    Loading comments...
  </div>

  <div v-else>



Year:  <USelect v-model="year" :options="years" />
Trip:  <USelect v-model="trip" :options="trips" />

    <UTable :columns="columns" :rows="data.pallets" />
  </div>
</template>
