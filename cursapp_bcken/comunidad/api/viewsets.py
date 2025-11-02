from rest_framework import viewsets, exceptions
from django.shortcuts import get_object_or_404
from comunidad.models import PreguntaForo, RespuestaForo
from cursos.models import Leccion, Modulo, Curso
from .serializers import PreguntaForoSerializer, RespuestaForoSerializer
from .permissions import IsEnrolledAndOwnerOrReadOnly

class PreguntaForoViewSet(viewsets.ModelViewSet):
    """
    Gestiona las Preguntas (hilos) del foro anidadas bajo una Lección.
    """
    serializer_class = PreguntaForoSerializer
    permission_classes = [IsEnrolledAndOwnerOrReadOnly]
    
    def get_queryset(self):
        # Filtra las preguntas para la lección específica en la URL
        leccion_pk = self.kwargs.get('leccion_pk')
        if leccion_pk:
            return PreguntaForo.objects.filter(leccion_id=leccion_pk)
        return PreguntaForo.objects.none()
    
    def perform_create(self, serializer):
        # Asigna el autor y la lección automáticamente
        leccion = get_object_or_404(Leccion, pk=self.kwargs.get('leccion_pk'))
        serializer.save(autor=self.request.user, leccion=leccion)
        
class RespuestaForoViewSet(viewsets.ModelViewSet):
    """
    Gestiona las Respuestas anidadas bajo una Pregunta.
    """
    serializer_class = RespuestaForoSerializer
    permission_classes = [IsEnrolledAndOwnerOrReadOnly]
    
    def get_queryset(self):
        pregunta_pk = self.kwargs.get('pregunta_pk')
        if pregunta_pk:
            return RespuestaForo.objects.filter(pregunta_id=pregunta_pk)
        return RespuestaForo.objects.none()
    
    def perform_create(self, serializer):
        pregunta = get_object_or_404(PreguntaForo, pk=self.kwargs.get('pregunta_pk'))
        
        # Valida el permiso para responder
        serializer.save(autor=self.request.user, pregunta=pregunta)
    
    # El instructor o autor de la pregunta marca como útil
    def update(self, request, *args, **kwargs):
        respuesta = self.get_object()
        
        # Solo el instructor del curso o el autor de la pregunta pueden marcar 'es_util'
        es_instructor = respuesta.pregunta.leccion.modulo.curso.instructor == request.user
        es_autor_pregunta = respuesta.pregunta.autor == request.user
        
        if 'es_util' in request.data and not (es_instructor or es_autor_pregunta):
            raise exceptions.PermissionDenied("Solo el instructor o el autor de la pregunta puede marcar esta respuesta.")
        
        return super().update(request, *args, **kwargs)