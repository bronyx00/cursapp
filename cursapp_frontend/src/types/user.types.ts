export enum UserRole {
    Admin = 1,
    Instructor = 2,
    Alumno = 3,
}

export interface UserProfile {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    bio: string | null;
    rol: UserRole;
    rol_display: string;
    foto_perfil: string | null;
    verificado: boolean;
    entidad_verificada: string | null;
    xp_totales?: string | number;
    puntos_totales: number;
}
