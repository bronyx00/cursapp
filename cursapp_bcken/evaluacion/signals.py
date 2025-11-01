from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProgresoLeccion, IntentoCuestionario, PuntosAlumno
from core.models import Usuario

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