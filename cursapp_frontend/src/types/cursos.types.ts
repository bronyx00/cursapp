export interface CursoList {
    id: number;
    titulo: string;
    slug: string;
    descripcion: string;
    instructor_nombre: string;
    promedio_calificacion_general: string;
    total_resenas: number;
    imagen_portada?: string;
}

export interface MiCursoInscrito {
    id: number;
    curso: CursoList;
    porcentaje_progreso: string;
    completado: boolean;
}