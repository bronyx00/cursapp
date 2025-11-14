export interface Categoria {
    id: number;
    nombre: string;
    slug: string;
    descripcion: string;
}

export interface CursoList {
    id: number;
    titulo: string;
    slug: string;
    descripcion: string;
    instructor_nombre: string;
    promedio_calificacion_general: string;
    total_resenas: number;
    portada: string | null;
    precio_usd: string;
    precio_ves: string | null;
    estado_display: string;
}

export interface MiCursoInscrito {
    id: number;
    curso: CursoList;
    porcentaje_progreso: string;
    completado: boolean;
}