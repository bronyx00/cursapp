<template>
    <div class="relative flex min-h-screen flex-col">
        <AnnouncementBar />
        <PublicNavbar />
        <main class="flex-1">
            <RouterView />
        </main>
        <PublicFooter />
    </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
import PublicNavbar from '@/components/shared/PublicNavbar.vue';
import PublicFooter from '@/components/shared/PublicFooter.vue';
import AnnouncementBar from '@/components/shared/AnnouncementBar.vue';
</script>