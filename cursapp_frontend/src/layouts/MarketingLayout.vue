<template>
    <div class="relative flex min-h-screen flex-col">
        <PublicNavbar />
        <main class="flex-1">
            <RouterView />
        </main>
    </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
import PublicNavbar from '@/components/shared/PublicNavbar.vue';

</script>