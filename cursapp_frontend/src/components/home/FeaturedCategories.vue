<template>
  <section class="container mx-auto overflow-hidden py-16 md:py-24">
    <div class="grid grid-cols-1 items-center gap-8 md:grid-cols-3 md:gap-16">
      
      <div class="max-w-xl md:col-span-1">
        <h2 class="text-3xl font-bold tracking-tighter text-foreground md:text-4xl">
          Aprende habilidades esenciales
        </h2>
        <p class="mt-4 text-lg text-muted-foreground">
          Desarrolla rápidamente las habilidades demandadas para impulsar tu carrera profesional en el cambiante mercado laboral.
        </p>
      </div>

      <div class="w-full md:col-span-2">
        <ul
          ref="scrollContainerRef"
          class="flex snap-x snap-mandatory gap-6 overflow-x-auto pb-6"
          :class="{
            '-mr-4 pr-4 md:-mr-0 md:pr-0': true // Compensación de padding solo en móvil
          }"
        >
          <template v-if="catalogStore.isLoading">
            <li v-for="i in 3" :key="i" class="w-3/4 flex-shrink-0 snap-start md:w-[calc((100%-48px)/3)]">
              <div class="h-96 w-full animate-pulse rounded-lg bg-muted"></div>
            </li>
          </template>
          
          <template v-else>
            <li
              v-for="cat in catalogStore.categorias"
              :key="cat.id"
              class="w-3/4 flex-shrink-0 snap-start md:w-[calc((100%-48px)/3)]"
            >
              <VerticalCategoryCard :categoria="cat" />
            </li>
          </template>
        </ul>
      </div>
    </div>

    <div class="hidden md:flex justify-center mt-8 gap-3">
      <Button @click="scrollPrev" variant="outline" size="icon" :disabled="arrivedState.left">
        <ChevronLeft class="h-5 w-5" />
        <span class="sr-only">Anterior</span>
      </Button>
      <Button @click="scrollNext" variant="outline" size="icon" :disabled="arrivedState.right">
        <ChevronRight class="h-5 w-5" />
        <span class="sr-only">Siguiente</span>
      </Button>
    </div>

  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useScroll } from '@vueuse/core';
import { useCatalogStore } from '@/store/catalog.store';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight } from 'lucide-vue-next';
import VerticalCategoryCard from './VerticalCategoryCard.vue'; 

const catalogStore = useCatalogStore();
const scrollContainerRef = ref<HTMLElement | null>(null);

// useScroll monitorea el contenedor
const { arrivedState } = useScroll(scrollContainerRef, {
  // Añadimos un offset para que los botones se desactiven
  // justo antes de llegar al borde exacto.
  offset: { left: 10, right: 10 } 
});

// --- LÓGICA DE SCROLL CORREGIDA (Scroll de 3 en 3) ---

const scrollNext = () => {
  if (!scrollContainerRef.value) return;
  // Mover una "página" completa (el ancho visible del contenedor)
  // que es exactamente 3 tarjetas gracias a nuestro CSS.
  const scrollAmount = scrollContainerRef.value.clientWidth;
  
  scrollContainerRef.value.scrollBy({ 
    left: scrollAmount, 
    behavior: 'smooth' // El movimiento "sutil"
  });
};

const scrollPrev = () => {
  if (!scrollContainerRef.value) return;
  const scrollAmount = scrollContainerRef.value.clientWidth;
  
  scrollContainerRef.value.scrollBy({ 
    left: -scrollAmount, 
    behavior: 'smooth' // El movimiento "sutil"
  });
};
// --- FIN DE LA CORRECCIÓN ---

onMounted(() => {
  catalogStore.fetchCategorias();
});
</script>

<style scoped>
/* Ocultar la barra de scroll */
.overflow-x-auto {
  scrollbar-width: none; /* Firefox */
}
.overflow-x-auto::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}
</style>