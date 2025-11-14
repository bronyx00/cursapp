<template>
  <div class="flex flex-col gap-8">
    
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold tracking-tight text-foreground md:text-4xl">
        Dashboard de Instructor
      </h1>
      <Button>
        <Plus class="mr-2 h-4 w-4" />
        Crear Nuevo Curso
      </Button>
    </div>

    <Card>
      <div class="grid grid-cols-1 md:grid-cols-3">
        <div class="p-6">
          <p class="text-sm font-medium text-muted-foreground">Ganancias Pendientes</p>
          <div v-if="instructorStore.isLoading" class="mt-1 h-8 w-1/2 animate-pulse rounded-md bg-muted"></div>
          <p v-else class="text-3xl font-bold tracking-tight text-primary">
            ${{ instructorStore.stats?.ganancias_pendientes_usd || '0.00' }}
          </p>
          <p class="text-xs text-muted-foreground">
            Total histórico: ${{ instructorStore.stats?.ganancias_totales_usd || '0.00' }}
          </p>
        </div>

        <div class="p-6 border-t md:border-l md:border-t-0">
          <p class="text-sm font-medium text-muted-foreground">Inscripciones Totales</p>
          <div v-if="instructorStore.isLoading" class="mt-1 h-8 w-1/2 animate-pulse rounded-md bg-muted"></div>
          <p v-else class="text-3xl font-bold tracking-tight">
            +{{ instructorStore.stats?.total_inscripciones || 0 }}
          </p>
          <p class="text-xs text-muted-foreground">
            en todos tus cursos
          </p>
        </div>

        <div class="p-6 border-t md:border-l md:border-t-0">
          <p class="text-sm font-medium text-muted-foreground">Reseñas Recibidas</p>
          <div v-if="instructorStore.isLoading" class="mt-1 h-8 w-1/2 animate-pulse rounded-md bg-muted"></div>
          <p v-else class="text-3xl font-bold tracking-tight">
            {{ instructorStore.stats?.total_resenas || 0 }}
          </p>
          <p class="text-xs text-muted-foreground">
            en todos tus cursos
          </p>
        </div>
      </div>
    </Card>

    <Card>
      <CardHeader>
        <CardTitle class="mt-3">Mis Cursos</CardTitle>
        <CardDescription>
          Aquí puedes ver, editar y gestionar todos los cursos que has creado.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Curso</TableHead>
              <TableHead>Estado</TableHead>
              <TableHead>Reseñas</TableHead>
              <TableHead class="text-right">Acciones</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <template v-if="instructorStore.isLoadingCursos">
              <TableRow v-for="i in 3" :key="i">
                <TableCell><div class="h-5 w-3/4 rounded-md bg-muted animate-pulse"></div></TableCell>
                <TableCell><div class="h-5 w-1/2 rounded-md bg-muted animate-pulse"></div></TableCell>
                <TableCell><div class="h-5 w-1/4 rounded-md bg-muted animate-pulse"></div></TableCell>
                <TableCell class="text-right"><div class="h-5 w-1/3 ml-auto rounded-md bg-muted animate-pulse"></div></TableCell>
              </TableRow>
            </template>
            
            <template v-else>
              <TableRow v-for="curso in instructorStore.misCursos" :key="curso.id">
                <TableCell class="font-medium">{{ curso.titulo }}</TableCell>
                <TableCell>
                  <span 
                    class="rounded-full px-2 py-0.5 text-xs font-medium"
                    :class="getEstadoBadgeClass(curso.estado_display)"
                  >
                    {{ curso.estado_display }}
                  </span>
                </TableCell>
                <TableCell>{{ curso.total_resenas }}</TableCell>
                <TableCell class="text-right">
                  <Button variant="outline" size="sm">
                    <Edit class="mr-2 h-3 w-3" />
                    Editar
                  </Button>
                </TableCell>
              </TableRow>
            </template>
            
            <TableRow v-if="!instructorStore.isLoadingCursos && instructorStore.misCursos.length === 0">
              <TableCell :colspan="4" class="py-12 text-center text-muted-foreground">
                Aún no has creado ningún curso.
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </CardContent>
    </Card>

  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useInstructorStore } from '@/store/instructor.store';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Plus, Edit } from 'lucide-vue-next';

const instructorStore = useInstructorStore();

onMounted(() => {
  instructorStore.fetchDashboardStats();
  instructorStore.fetchMisCursos();
});

// Helper para dar color a los 'badges' de estado
const getEstadoBadgeClass = (estado?: string) => {
  if (estado === 'Publicado') {
    return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200';
  }
  if (estado === 'Borrador') {
    return 'bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200';
  }
  return 'bg-muted text-muted-foreground';
};
</script>