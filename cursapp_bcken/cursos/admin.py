from django.contrib import admin
from .models import Categoria, Etiqueta, Curso, Modulo, Leccion, Cupon

# --- Inlines (para edición anidada) ---
class LeccionInline(admin.TabularInline):
    """PErmite editar Lecciones dewntro de la vista de Módulo."""
    model = Leccion
    extra = 1 # Mostrar 1 slot para nueva lección
    ordering = ('orden',)
    
class ModuloInline(admin.StackedInline):
    """Permite editar Módulos dentro de la vista de Curso."""
    model = Modulo
    extra = 1 # Mostrar 1 slot para nuevo módulo
    ordering = ('orden',)
    inlines = [LeccionInline]
    
# --- ModelAdmins Principales ---

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    """
    Configuración robusta para el Admin de Cursos.
    """
    list_display = (
        'titulo',
        'instructor',
        'estado',
        'precio_usd',
        'total_resenas',
        'promedio_calificacion_general'
    )
    list_filter = ('estado', 'categoria', 'instructor')
    search_fields = ('titulo', 'instructor__username','slug')
    
    # Rellenar automáticamente el slug a partir del título
    prepopulated_fields = {'slug': ('titulo',)}
    
    # Campos de solo lectura
    readonly_fields = (
        'total_resenas',
        'promedio_calificacion_general', 
        'promedio_calidad_contenido',
        'promedio_claridad_explicacion',
        'promedio_utilidad_practica',
        'promedio_soporte_instructor'
    )
    
    # Añadir Módulos en la misma página de edicion del Curso
    inlines = [ModuloInline]
    
    fieldsets = (
        (None, {
            'fields': ('titulo', 'slug', 'instructor', 'estado')
        }),
        ('Contenido y Taxonomía', {
            'fields': ('descripcion', 'categoria', 'etiquetas')
        }),
        ('Monetización', {
            'fields': ('precio_usd', 'req_certificado')
        }),
        ('Calificaciones (Solo Lectura)', {
            'classes': ('collapse',), # Ocultar por defecto
            'fields': (
                'total_resenas', 
                'promedio_calificacion_general',
                'promedio_calidad_contenido',
                'promedio_claridad_explicacion',
                'promedio_utilidad_practica',
                'promedio_soporte_instructor'
            ),
        }),
    )

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    """Admin para gestionar Módulos (Si se accede directamente)."""
    list_display = ('titulo', 'curso', 'orden')
    list_filter = ('curso',)
    search_fields = ('titulo', 'curso__titulo')
    ordering = ('curso', 'orden')
    inlines = [LeccionInline]
    
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    
@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    
@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'instructor',
        'porcentaje_descuento',
        'esta_activo',
        'usos_actuales',
        'usos_maximos'
    )
    list_filter = ('instructor', 'fecha_expiracion')
    search_fields = ('codigo', 'instructor__username')
    readonly_fields = ('usos_actuales',)
    
admin.site.register(Leccion)