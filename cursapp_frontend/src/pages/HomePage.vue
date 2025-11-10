<template>
    <div class="bg-background text-foreground">
        <HeroSection />
        <FeaturedCategories />
        <PopularCourses />
        <TestimonialsSection />
        <SocialProofLogos />
        

        <section class="container mx-auto px-4 py-24 md:py-32">
            <div class="mx-auto max-w-3xl text-center">
                <h2 class="text-4xl font-bold tracking-tighter text-foreground md:text-5xl">
                    Conviértete en Instructor
                </h2>
                <p class="mt-6 text-lg text-muted-foreground md:text-xl">
                    Comparte tu conocimiento con miles de estudiantes y genera ingresos. Te proveemos las herramientas para crear cursos de clase mundial.
                </p>
                <Button size="lg" class="mt-10">
                    Empieza a enseñar hoy
                </Button>
            </div>
        </section>
    </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useCatalogStore } from '@/store/catalog.store';
import Button from '@/components/ui/button/Button.vue'
import FeaturedCategories from '@/components/home/FeaturedCategories.vue'; 
import HeroSection from '@/components/home/HeroSection.vue';
import PopularCourses from '@/components/home/PopularCourses.vue';
import SocialProofLogos from '@/components/home/SocialProofLogos.vue';
import TestimonialsSection from '@/components/home/TestimonialsSection.vue';

const catalogStore = useCatalogStore();

onMounted(() => {
catalogStore.fetchCursos();
});
</script>