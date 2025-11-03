from django.contrib import admin
from .models import (
    Inscripcion, Transaccion, Resena, Cuestionario, Pregunta,
    ProgresoLeccion, Certificado, Insignia, PuntosAlumno
)

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    """
    Permite al Admin gestionar inscripciones.
    """
    list_display = (
        'id',
        'alumno',
        'curso',
        'estado_pago',
        'precio_pagado_usd',
        'fecha_inscripcion'
    )
    list_filter = ('estado_pago', 'curso')
    search_fields = ('alumno__username', 'curso__titulo', 'referencia_pago')
    list_editable = ('estado_pago',) # Permite editar el estado desde la DB, cambiar luego!!
    readonly_fields = ('fecha_inscripcion',)
    autocomplete_fields = ('alumno', 'curso') # Optimiza la búsqueda
    
@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    """
    Permite al Admin gestionar los pagos a instructores.
    """
    list_display =(
        'id',
        'get_instructor',
        'monto_total_usd',
        'monto_instructor_usd',
        'estado_pago_instructor',
        'fecha_creacion'
    )
    list_filter = ('estado_pago_instructor',)
    search_fields = ('inscripcion__curso__instructor__username', 'inscripcion__alumno__username')
    list_editable = ('estado_pago_instructor',)
    readonly_fields = (
        'inscripcion',
        'monto_total_usd',
        'comision_plataforma_usd',
        'monto_instructor_usd',
        'comision_aplicada_porcentaje',
        'fecha_creacion'
    )
    
    @admin.display(description='Instructor')
    def get_instructor(self, obj):
        if obj.inscripcion and obj.inscripcion.curso:
            return obj.inscripcion.curso.instructor
        return 'N/A'

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    """Admin para moderar reseñas."""
    list_display = ('get_curso', 'get_alumno', 'calificacion_general', 'fecha_creacion')
    search_fields = ('inscripcion__alumno__username', 'inscripcion__curso__titulo', 'comentario')
    readonly_fields = ('inscripcion', 'fecha_creacion', 'fecha_actualizacion')
    
    @admin.display(description='Curso')
    def get_curso(self, obj):
        return obj.inscripcion.curso.titulo
    
    @admin.display(description='Alumno')
    def get_alumno(self, obj):
        return obj.inscripcion.alumno.username
    
admin.site.register(Certificado)
admin.site.register(Insignia)
admin.site.register(Cuestionario)
admin.site.register(Pregunta)
admin.site.register(PuntosAlumno)
admin.site.register(ProgresoLeccion)
