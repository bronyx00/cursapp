<template>
    <section class="py-16 md:py-24">
        <div class="container mx-auto px-4">

            <Tabs default-value="populares" class="w-full">
                <div class="flex flex-col items-center gap-4 md:flex-row md:justify-between">
                    <div>
                        <h2 class="text-3xl md:text-4xl font-bold tracking-tight text-foreground text-center md:text-left">
                            Una amplia selección de cursos
                        </h2>
                        <p class="mt-2 text-lg text-muted-foreground text-center md:text-left">
                            Explora nuestros cursos más populares y los últimos lanzamientos.
                        </p>
                    </div>
                    <TabsList class="shrink-0">
                        <TabsTrigger value="populares">
                            Populares
                        </TabsTrigger>
                        <TabsTrigger value="nuevos">
                            Últimos lanzamientos
                        </TabsTrigger>
                    </TabsList>
                </div>

                <TabsContent value="populares">
                    <div v-if="catalogStore.isLoading" class="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                        <CourseCardSkeleton v-for="i in 8" :key="i" :class="[ i >= 4 ? 'hidden sm:block' : '' ]" />
                    </div>
                    <div v-else-if="catalogStore.popularCourses.length > 0" class="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                        <CourseCard
                            v-for="(curso, index) in catalogStore.popularCourses.slice(0, 8)"
                            :key="curso.id"
                            :curso="curso"
                            :progreso="'0'"
                            :show-progress="false"
                            :show-price="true"
                            :class="[ index >= 4 ? 'hidden sm:block' : '' ]"
                        />
                    </div>
                    <div v-else class="mt-10 text-center text-muted-foreground">
                        <p>No se encontraron cursos populares.</p>
                    </div>
                </TabsContent>

                <TabsContent value="nuevos">
                    <div v-if="catalogStore.isLoading" class="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                        <CourseCardSkeleton v-for="i in 4" :key="i" :class="[ i >= 4 ? 'hidden sm:block' : '' ]" />
                    </div>
                    <div v-else-if="catalogStore.newCourses" class="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                        <CourseCard
                            v-for="(curso, index) in catalogStore.newCourses.slice(0, 8)"
                            :key="curso.id"
                            :curso="curso"
                            :progreso="'0'"
                            :show-progress="false"
                            :show-price="true"
                            :class="[ index >= 4 ? 'hidden sm:block' : '' ]"
                        />
                    </div>
                    <div v-else class="mt-10 text-center text-muted-foreground">
                        <p>No se encontraron cursos nuevos.</p>
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs/';
import { useCatalogStore } from '@/store/catalog.store';
import CourseCard from '@/components/shared/CourseCard.vue';
import CourseCardSkeleton from '@/components/shared/CourseCardSkeleton.vue';

const catalogStore = useCatalogStore();

onMounted(() => {
    catalogStore.fetchPopularCourses();
    catalogStore.fetchNewCourses();
})
</script>