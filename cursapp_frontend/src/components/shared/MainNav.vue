<template>
    <nav class="flex flex-col gap-2" @click="onLinkClick">
        <RouterLink to="/mi-aprendizaje" custom v-slot="{ isActive, href, navigate }">
            <a 
                :href="href",
                @click="navigate"
                class="flex items-center gap-3 rounded-lg px-3 py-2 text-base font-medium transition-all"
                :class="isActive
                    ? 'bg-secondary text-primary-foreground'
                    : 'text-secondary-foreground hover:bg-secondary/50'"
            >
            <LayoutDashboard class="h-5 w-5" />
                Mi Aprendizaje
        </a>
        </RouterLink>

        <RouterLink to="/leaderboard" custom v-slot="{ isActive, href, navigate }">
            <a 
                :href="href"
                @click="navigate"
                class="flex items-center gap-3 rounded-lg px-3 py-2 text-base font-medium transition-all"
                :class="isActive
                    ? 'bg-secondary text-primary-foreground'
                    : 'text-secondary-foreground hover:bg-secondary/50'"
            >
            <Trophy class="h-5 w-5" />
                Leaderboard
            </a>
        </RouterLink>
    </nav>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { LayoutDashboard, Trophy } from 'lucide-vue-next';

// Emitirá un evento para cerrar el menú móvil cuando se haga click en un enlace
const emit = defineEmits(['navigated'])

const onLinkClick = () => {
    emit('navigated');
}

</script>