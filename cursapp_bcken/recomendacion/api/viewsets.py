from rest_framework import generics, permissions
from recomendacion.api.serializers import CursoListSerializer
from cursos.models import Curso
from evaluacion.models import InteraccionLeccion, Inscripcion
from django.db.models import Count

class RecomendacionAPIView(generics.ListAPIView):
    """
    ENDPOINT PRINCIPAL DEL MOTOR DE RECOMENDACIÓN.
    Devuelve cursos recomendados basados en el perfil y actividad del usuario.
    """
    serializer_class = CursoListSerializer
    # Las recomendaciones son personalizadas, solo para usuarios autenticados.
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Identificar cursos ya inscritos (para excluirlos)
        cursos_inscritos_ids = Inscripcion.objects.filter(
            alumno=user,
            estado_pago=Inscripcion.ESTADO_PAGADO
        ).values_list('curso_id', flat=True)
        
        # Análisis de Comportamiento
        # Buscar la categoría donde el usuario tuvo la mayor interacción (tasa_interes > 0)
        afinidades = InteraccionLeccion.objects.filter(
            alumno=user,
            tasa_interes__gt=0 # Solo interacciones positivas/completadas
        ).values(
            'leccion__modulo__curso__categoria' # Agrupar por la categoría del curso
        ).annotate(
            total_interacciones=Count('leccion__modulo__curso__categoria')
        ).order_by('-total_interacciones').first()
        
        recomendaciones = Curso.objects.none() # QuerySet vacío inicial
        
        if afinidades:
            # Recomendar 3 cursos de la categoría más afín (la primera en afinidades).
            categoria_preferida_id = afinidades[0]['leccion__modulo__curso__categoria']
            
            recomendaciones = Curso.objects.filter(
                estado=Curso.ESTADO_PUBLICADO,
                categoria_id=categoria_preferida_id
            ).exclude(
                id__in=cursos_inscritos_ids # Excluir cursos ya comprados
            ).order_by('?')[:3]
            
            # Si se encuentran cursos, devolver estas 3 recomendaciones.
            
            if recomendaciones.exists():
                return recomendaciones
            
        # Cold Start: Si no hay cursos en la categoría afín, devuelve los cursos más recientes
        return Curso.objects.filter(
            estado=Curso.ESTADO_PUBLICADO
        ).exclude(
            id__in=cursos_inscritos_ids
        ).order_by('-fecha_creacion')[:5]