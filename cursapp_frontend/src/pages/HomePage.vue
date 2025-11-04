<template>
    <div class="text-center">
        <h1 class="text-3xl font-bold">Bienvenido a CursApp</h1>
        <p class="mt-2 text-slate-600 dark:text-slate-400">Crear slogan para la plataforma.</p>
        <Button as-child class="mt-4">
            <RouterLink to="/login">Comenzar</RouterLink>
        </Button>
    </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
import Button from '@/components/ui/button/Button.vue'
</script>