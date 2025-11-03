from rest_framework import permissions
from evaluacion.models import Inscripcion
from comunidad.models import PreguntaForo

class IsEnrolledAndOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso de alto nivel para la comindad (Q&A).
    - LECTURA (GET): Permitido si el usuario está inscrito y pagado.
    - ESCRITURA (POST): Permitido si el usuario está inscrito y pagado.
    - EDICIÓN (PUT/DELETE): Permitido solo si el usuario es el AUTOR.
    """
    
    def has_permission(self, request, view):
        # Autenticación básica
        if not request.user.is_authenticated:
            return False
        
        # Permisos de Lectura
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permisos de Escritura
        # Verificamos que el usuario esté inscrito en el curso asociado
        leccion_id = view.kwargs.get('leccion_pk')
        pregunta_id = view.kwargs.get('pregunta_pk')
        
        if not leccion_id and not pregunta_id:
            return False
        
        if pregunta_id:
            # Si estamos creando una RESPUESTA, buscamos la lección a través de la pregunta
            try:
                leccion_id = PreguntaForo.objects.get(pk=pregunta_id).leccion.id
            except PreguntaForo.DoesNotExist:
                return False
        
        # Verificar la inscripción
        esta_inscrito = Inscripcion.objects.filter(
            alumno=request.user,
            curso__modulos__lecciones__id=leccion_id,
            estado_pago=Inscripcion.ESTADO_PAGADO
        ).exists()
        
        return esta_inscrito
    
    def has_object_permission(self, request, view, obj):
        # Permisos de Lectura
        if request.method in permissions.SAFE_METHODS:
            # Verificamos si el usuario puede ver este objeto (si está inscrito)
            curso = None
            if hasattr(obj, 'leccion'): # Si es una Pregunta
                curso = obj.leccion.modulo.curso
            elif hasattr(obj, 'pregunta'): # Si es una Respuesta
                curso = obj.pregunta.leccion.modulo.curso
                
            if not curso:
                return False
            
            return Inscripcion.objects.filter(
                alumno=request.user,
                curso=curso,
                estado_pago=Inscripcion.ESTADO_PAGADO
            ).exists()
            
        # Permisos de Edición/Borrado
        # Solo el autor original puede editar o borrar
        return obj.autor == request.user