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
        
        # Caso Cold Start (Usuario Nuevo) o Sin Interacciones
        # Si el usuario no tiene historial, recomendaremos los cursos más populares o recientes.
        if not InteraccionLeccion.objects.filter(alumno=user).exists():
            # Recomendación por popularidad (simulada por mayor número de inscripciones en un futuro)
            # Por ahora, más recientes:
            return Curso.objects.filter(estado=Curso.ESTADO_PUBLICADO).order_by('-fecha_creacion')[:5]
        
        # LÓGICA DE INFERENCIA (Filtración Basada en Comportamiento)
        
        # Aquí se conectará el modelo de IA o Machine Learning
        
        # SIMULACION: encuentra la categoria favorita del usuario
        categoria_favorita_id = InteraccionLeccion.objects.filter(alumno=user, tasa_interes=1).values_list(
            'leccion__modulo__curso__categoria', flat=True
        ).annotate(
            count=Count('leccion__modulo__curso__categoria')
        ).order_by('-count').first()
        
        if categoria_favorita_id:
            # Recomendamos otros cursos de su categoría favorita
            return Curso.objects.filter(
                estado=Curso.ESTADO_PUBLICADO,
                categoria_id=categoria_favorita_id
            ).exclude(
                inscripcion__alumno=user,
                inscripcion__estado_pago=Inscripcion.ESTADO_PAGADO
            ).order_by('?')[:5] # '?' = orden aleatorio para simular variedad
            
        return Curso.objects.filter(estado=Curso.ESTADO_PUBLICADO).order_by('-fecha_creacion')[:5]