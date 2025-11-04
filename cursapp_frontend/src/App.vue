<template>
  <RouterView />
</template>


<script setup lang="ts">
import { onMounted } from 'vue';
import { RouterView } from 'vue-router';

onMounted(() => {
  document.documentElement.classList.add('dark');
});
</script>