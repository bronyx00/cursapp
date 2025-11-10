<template>
  <section class="py-16 md:py-24 bg-secondary/50">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl md:text-4xl font-bold tracking-tighter text-foreground text-center">
        Lo que dicen nuestros alumnos
      </h2>
      <p class="mt-4 text-lg text-muted-foreground text-center max-w-2xl mx-auto">
        Miles de estudiantes han usado CursApp para conseguir el trabajo de sus sueños,
        escalar en su carrera o iniciar un nuevo hobby.
      </p>

      <div class="w-full max-w-full mt-12">
        <ul class="flex snap-x snap-mandatory gap-6 overflow-x-auto pb-6 -mx-4 px-4">
          
          <li v-for="testimonial in testimonials" :key="testimonial.name"
            class="w-4/5 flex-shrink-0 snap-start md:w-[calc((100%-48px)/3)]"
          >
            <div class="flex h-full flex-col justify-between rounded-lg border bg-card p-6 shadow-sm">
              <blockquote class="text-lg text-foreground">
                "{{ testimonial.quote }}"
              </blockquote>
              <footer class="mt-6 flex items-center gap-3">
                <Avatar class="h-12 w-12">
                  <AvatarImage :src="testimonial.avatar" :alt="testimonial.name" />
                  <AvatarFallback>{{ testimonial.name.substring(0, 2) }}</AvatarFallback>
                </Avatar>
                <div>
                  <div class="font-semibold text-foreground">{{ testimonial.name }}</div>
                  <div class="text-sm text-muted-foreground">{{ testimonial.title }}</div>
                </div>
              </footer>
            </div>
          </li>

        </ul>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'

// Data de ejemplo. En el futuro, esto debería venir de tu API de Reseñas.
const testimonials = [
  {
    name: "Ana Pérez",
    title: "Desarrolladora Frontend",
    avatar: "https://i.pravatar.cc/150?img=1",
    quote: "CursApp fue un cambio de juego. Pasé de cero a tener un portafolio y conseguir mi primer trabajo en 6 meses. 100% recomendado."
  },
  {
    name: "Carlos Rodríguez",
    title: "Estudiante de Data Science",
    avatar: "https://i.pravatar.cc/150?img=3",
    quote: "La calidad del contenido es de primera. Los instructores explican conceptos complejos de forma clara y directa al grano. Justo lo que necesitaba."
  },
  {
    name: "Sofía Martínez",
    title: "Diseñadora UX/UI",
    avatar: "https://i.pravatar.cc/150?img=5",
    quote: "Me encantó la flexibilidad. Pude aprender a mi propio ritmo, y la comunidad en los foros siempre estuvo ahí para ayudar."
  },
  {
    name: "Miguel González",
    title: "Ingeniero de Software en Google",
    avatar: "https://i.pravatar.cc/150?img=8",
    quote: "Como instructor, la plataforma me da todas las herramientas para publicar mi contenido fácilmente y conectar con mis estudiantes."
  }
];
</script>

<style scoped>
/* Ocultar la barra de scroll */
.overflow-x-auto {
  scrollbar-width: none;
}
.overflow-x-auto::-webkit-scrollbar {
  display: none;
}
</style>