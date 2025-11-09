<template>
    <div v-if="isVisible" class="relative w-full bg-primary py-2 px-4 text-primary-foreground">
        <div class="container mx-auto flex items-center justify-center text-center text-sm font-medium">
            <p>
                <span class="mr-2 inline-block rounded-full bg-primary-foreground/20 px-2 py-0.5 text-xs font-semibold">
                    NUEVO
                </span>
                ¡Planes de suscripción ya disponibles! Ahorra un 20% este mes.
            </p>
            <button
                @click="isVisible = false"
                class="absolute top-1/2 right-4 -translate-y-1/2 rounded-full p-1 text-primary-foreground/70 transition-colors hover:text-primary-foreground"
            >
                <X class="h-4 w-4" />
                <span class="sr-only">Cerrar anuncio</span>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { X } from 'lucide-vue-next';

const isVisible = ref(true);
</script>