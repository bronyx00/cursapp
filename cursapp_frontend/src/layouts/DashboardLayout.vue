<template>
    <div class="grid min-h-screen w-full lg:grid-cols-[280px_1fr]">
        
        <aside class="hidden border-r bg-secondary/20 lg:block">
            <div class="flex h-full max-h-screen flex-col gap-2">
                <div class="flex h-16 items-center border-b px-6">
                    <RouterLink to="/" class="flex items-center gap-2">
                        <BookMarked class="h-6 w-6 text-primary" />
                        <span class="text-lg font-semibold">CursApp</span>
                    </RouterLink>
                </div>

                <div class="flex-1 overflow-auto py-2">
                    <MainNav class="px-4" />
                </div>

                <div class="mt-auto border-t p-4">
                    <UserNav />
                </div>
            </div>
        </aside>

        <div class="flex flex-col">
            <header class="flex h-16 items-center gap-4 border-b bg-background px-4 lg:hidden">
                <Sheet v-model:open="isMobileMenuOpen">
                    <SheetTrigger as-child>
                        <Button variant="outline" size="icon" class="shrink-0">
                            <Menu class="h-5 w-5" />
                            <span class="sr-only">Abrir Menú de navegación</span>
                        </Button>
                    </SheetTrigger>
                    <SheetContent side="left" class="flex flex-col">
                        <SheetHeader class="border-b pb-4">
                            <RouterLink to="/" class="flex items-center gap-2">
                                <BookMarked class="h-6 w-6 text-primary" />
                                <span class="text-lg font-semibold">CursApp</span>
                            </RouterLink>
                        </SheetHeader>
                        <MainNav class="mt-4" @navigated="isMobileMenuOpen = false" />
                    </SheetContent>
                </Sheet>

                <div class="ml-auto">
                    <UserNav />
                </div>
            </header>

            <main class="flex-1 overflow-auto p-4 sm:p-6 lg:p-8">
                <RouterView />
            </main>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import { BookMarked, Menu } from 'lucide-vue-next';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetHeader, SheetTrigger } from '@/components/ui/sheet';

import MainNav from '@/components/shared/MainNav.vue';
import UserNav from '@/components/shared/UserNav.vue';

const isMobileMenuOpen = ref(false);
</script>