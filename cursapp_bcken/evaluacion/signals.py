from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProgresoLeccion, IntentoCuestionario, PuntosAlumno, Resena, Inscripcion, Transaccion
from django.db.models import Avg, Count
from core.models import Usuario
from decimal import Decimal

@receiver(post_save, sender=ProgresoLeccion)
def otorgar_xp_por_leccion(sender, instance, created, **kargs):
    """
    Otorga XP automáticamente cuando una lección se marca como completada
    por primera vez
    """
    # Si la lección está completada y no es la primera vez se guarda (para evitar dobles puntos)
    if instance.completado and not created:
        # Verificar si ya dimos XP por esta lección (para evitar trampas)
        progreso_anterior = ProgresoLeccion.objects.get(pk=instance.pk)
        if not progreso_anterior.completado: # Si NO estaba completada antes
            usuario = instance.inscripcion.alumno
            usuario.xp_totales += 10 # Otorga 10 XP
            usuario.save(update_fields=['xp_totales'])
            
@receiver(post_save, sender=IntentoCuestionario)
def otorgar_xp_por_cuestionario(sender, instance, created, **kargs):
    """
    Otorga XP si el cuestionario es aprobado.
    """
    if instance.aprobado and created:
        usuario = instance.inscripciones.alumno
        usuario.xp_totales +=50
        usuario.save(update_fields=['xp_totales'])
        
@receiver(post_save, sender=PuntosAlumno)
def actualizar_puntos_totales(sender, instance, created, **kargs):
    """
    Mantiene sincronizado el campo 'puntos_totales' del Usuario
    con cada transacción en Puntos Alumno.
    """
    if created:
        usuario = instance.alumno
        # Suma (o resta) los puntos de la transacción al total del usuario
        usuario.puntos_totales += instance.puntos
        usuario.save(update_fields=['puntos_totales'])
        
def recalcular_calificaciones_curso(curso_id):
    """
    Función helper para recalcular y guardar los promedios de
    calificación en el modelo Curso.
    """
    from cursos.models import Curso
    
    # Obtener todas las reseñas activas de un curso
    resenas = Resena.objects.filter(inscripcion__curso_id=curso_id)
    
    if resenas.exists():
        # Calcular los agregados (promedios y conteo)
        agregados = resenas.aggregate(
            total=Count('id'),
            prom_general=Avg('calificacion_general'),
            prom_contenido=Avg('calificacion_calidad_contenido'),
            prom_explicacion=Avg('calificacion_claridad_explicacion'),
            prom_utilidad=Avg('calificacion_utilidad_practica'),
            prom_soporte=Avg('calificacion_soporte_instructor')
        )
        
        # Actualizar el curso con los nuevos promedios
        Curso.objects.filter(pk=curso_id).update(
            total_resenas=agregados['total'],
            promedio_calificacion_general=round(agregados['prom_general'], 2),
            promedio_calidad_contenido=round(agregados['prom_contenido'], 2),
            promedio_claridad_explicacion=round(agregados['prom_explicacion'], 2),
            promedio_utilidad_practica=round(agregados['prom_utilidad'], 2),
            promedio_soporte_instructor=round(agregados['prom_soporte'], 2)
        )
    else:
        # Si no quedan reseñas (ej. se borró la última), resetear
        Curso.objects.filter(pk=curso_id).update(
            total_resenas=0,
            promedio_calificacion_general=0.00,
            promedio_calidad_contenido=0.00,
            promedio_claridad_explicacion=0.00,
            promedio_utilidad_practica=0.00,
            promedio_soporte_instructor=0.00
        )
        
@receiver(post_save, sender=Resena)
def actualizar_promedios_on_save(sender, instance, **kargs):
    """
    Cuando una Reseña se crea o actualiza, recalcula los promedios del curso.
    """
    recalcular_calificaciones_curso(instance.inscripcion.curso.id)
    
@receiver(post_delete, sender=Resena)
def actualizar_promedios_on_delete(sender, instance, **kargs):
    """
    Cuando una Reseña se elimina, recalcula los promedios del curso.
    """
    recalcular_calificaciones_curso(instance.inscripcion.curso.id)
    
@receiver(post_save, sender=Inscripcion)
def crear_transaccion_post_inscripcion(sender, instance, created, **kwargs):
    """
    Crea un registro de Transacción cuando una Inscripción se marca como PAGADA.
    Esto ocurre después de que la pasarela de pago confirma la compra.
    """
    # Si la inscripción está PAGADA y (es nueva O cambió de estado)
    if instance.estado_pago == Inscripcion.ESTADO_PAGADO:
        # Verificar si ya existe una transacción para evitar duplicados
        if hasattr(instance, 'transaccion'):
            return # La transacción ya existe, no hacer nada
        
        # Obtener datos para el cálculo
        monto_total = instance.precio_pagado_usd
        instructor = instance.curso.instructor
        
        # Obtener comisión (del perfil del instructor)
        comision_porcentaje = instructor.comision if instructor else Decimal('100.00') # 100% Si no hay instructor
        comision_decimal = comision_porcentaje / Decimal('100.00')
        
        # Calcular montos
        comision_plataforma = monto_total * comision_decimal
        monto_instructor = monto_total - comision_plataforma
        
        # Crear la Transacción
        Transaccion.objects.create(
            inscripcion=instance,
            monto_total_usd=monto_total,
            comision_plataforma_usd=comision_plataforma,
            monto_instructor_usd=monto_instructor,
            comision_aplicada_porcentaje=comision_porcentaje,
            estado_pago_instructor=Transaccion.ESTADO_PENDIENTE
        )