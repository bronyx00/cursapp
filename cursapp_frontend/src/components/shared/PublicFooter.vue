<template>
  <footer class="border-t bg-background">
    <div class="container mx-auto px-4 py-16">
      <div class="grid grid-cols-2 gap-12 md:grid-cols-5">
        
        <div class="col-span-2 md:col-span-2">
          <RouterLink to="/" class="flex items-center gap-2">
            <span class="text-2xl font-bold tracking-tight">cursapp</span>
          </RouterLink>
          <p class="mt-4 max-w-xs text-muted-foreground">
            Habilidades reales, rápido. Domina las tecnologías más demandadas.
          </p>
        </div>

        <div class="col-span-1">
          <h4 class="font-semibold text-foreground">Cursos</h4>
          <nav class="mt-4 flex flex-col gap-2">
            <RouterLink to="/categorias/desarrollo-web" class="text-muted-foreground hover:text-primary">
              Desarrollo Web
            </RouterLink>
            <RouterLink to="/categorias/desarrollo-movil" class="text-muted-foreground hover:text-primary">
              Desarrollo Móvil
            </RouterLink>
            <RouterLink to="/categorias/data-science" class="text-muted-foreground hover:text-primary">
              Data Science
            </RouterLink>
            <RouterLink to="/categorias/ia" class="text-muted-foreground hover:text-primary">
              Inteligencia Artificial
            </RouterLink>
          </nav>
        </div>

        <div class="col-span-1">
          <h4 class="font-semibold text-foreground">CursApp</h4>
          <nav class="mt-4 flex flex-col gap-2">
            <RouterLink to="/nosotros" class="text-muted-foreground hover:text-primary">
              Sobre Nosotros
            </RouterLink>
            <RouterLink to="/instructores" class="text-muted-foreground hover:text-primary">
              Enseña en CursApp
            </RouterLink>
            <RouterLink to="/blog" class="text-muted-foreground hover:text-primary">
              Blog
            </RouterLink>
          </nav>
        </div>

        <div class="col-span-1">
          <h4 class="font-semibold text-foreground">Soporte</h4>
          <nav class="mt-4 flex flex-col gap-2">
            <RouterLink to="/contacto" class="text-muted-foreground hover:text-primary">
              Contacto
            </RouterLink>
            <RouterLink to="/privacidad" class="text-muted-foreground hover:text-primary">
              Privacidad
            </RouterLink>
            <RouterLink to="/terminos" class="text-muted-foreground hover:text-primary">
              Términos
            </RouterLink>
          </nav>
        </div>

      </div>

      <div class="mt-12 flex flex-col items-center justify-between border-t pt-8 md:flex-row">
        <p class="text-sm text-muted-foreground">
          &copy; {{ new Date().getFullYear() }} CursApp. Todos los derechos reservados.
        </p>
        <div class="mt-4 flex items-center gap-4 md:mt-0">
          <a href="#" class="text-muted-foreground hover:text-primary">
            <span class="sr-only">X (Twitter)</span>
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
          </a>
          <a href="#" class="text-muted-foreground hover:text-primary">
            <span class="sr-only">LinkedIn</span>
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" clip-rule="evenodd"/></svg>
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
</script>