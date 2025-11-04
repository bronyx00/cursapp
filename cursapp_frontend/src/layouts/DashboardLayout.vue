<template>
    <div class="flex max-h-screen w-full">
        <aside class="w-64 border-r bg-slate-50 dark:border-slate-800 dark:bg-slate-900">
            <div class="p-4">
                <h2 class="text-xl font-bold">cursapp</h2>
            </div>
            <nav class="flex flex-col p-4">
                <RouterLink to="/mi-aprendizaje" class="rounded p-2 hover:bg-slate-200 dark:hover:bg-slate-800">
                    Mi Aprendizaje
                </RouterLink>
                <a @click="onLogout" class="mt-4 cursor-pointer rounded p-2 text-red-500 hover:bg-slate-200 dark:hover:bg-slate-800">
                    Cerrar Sesión
                </a>
            </nav>
        </aside>

        <main class="flex-1 bg-slate-100 p-8 dark:bg-slate-950">
            <RouterView />
        </main>
    </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView, useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth.store';

const authStore = useAuthStore();
const router = useRouter();

const onLogout = () => {
    authStore.logout();
}
</script>