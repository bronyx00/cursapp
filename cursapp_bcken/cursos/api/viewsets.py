from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from django.db.models import Count
from cursos.models import Curso, Modulo, Leccion, Categoria, Cupon
from .serializers import CursoListSerializer, CursoDetailSerializer, ModuloSerializer, LeccionSerializer, CategoriaSerializer, CuponSerializer
from cursos.tasks import process_video_task

# --- Permisos Personalizados ---
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso de alto nivel para todo el contenido de 'cursos'.
    - Permite lectura (GET) a todos.
    - Permite CREAR (POST) solo a Instructores.
    - Permite EDITAR/BORRAR (PUT/DELETE) solo al Instructor PROPIETARIO
    """
    def has_permission(self, request, view):
        # Permite lectura a cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Deniega escritura a usuarios no autenticados
        if not request.user.is_authenticated:
            return False
        
        # Permite CREAR solo si es Instructor
        return request.user.es_instructor
    
    def has_object_permission(self, request, view, obj):
        # Permite lectura a cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Deniega si no es instructor
        if not request.user.es_instructor:
            return False
        
        # Determinar el propietario
        owner = None
        if isinstance(obj, Curso):
            # Si el objeto es un Curso, el dueño es 'instructor'
            owner = obj.instructor
        elif isinstance(obj, Modulo):
            # Si el objeto es un Modulo, el dueño es 'curso.instructor'
            owner = obj.curso.instructor
        elif isinstance(obj, Leccion):
            # Si el objeto es una Leccion, el dueño es 'modulo.curso.instructor'
            owner = obj.modulo.curso.instructor
            
        # Permitir solo si el usuario es el propietario
        return owner == request.user
    
# --- ViewSets ---
class CursoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar y recuperar cursos (Catálogo) y gestionarlos (CRUD).
    - El público general solo ve cursos PUBLICADOS.
    - El instructor propietario ve TODOS sus cursos (Borrador, Publicado, Suspendido).
    """
    queryset = Curso.objects.all().order_by('-fecha_creacion')
    permission_classes = [IsOwnerOrReadOnly] # Lectura pública, escritura solo para Instructores.
    
    def get_serializer_class(self):
        """Alterna entre el serializer de listado y el de detalle."""
        if self.action == 'list':
            return CursoListSerializer
        return CursoDetailSerializer
        
    def get_queryset(self):
        """
        Filtra dinámicamente los cursos visibles basado en el rol del usuario.
        """
        user = self.request.user
        
        # Si el usuario no está autenticado O no es instructor
        if not user.is_authenticated or not user.es_instructor:
            # Mostrar solo cursos PUBLICADOS
            return self.queryset.filter(estado=Curso.ESTADO_PUBLICADO)
        
        # Si el usuario es instructor
        from django.db.models import Q
        
        return self.queryset.filter(
            Q(instructor=user) | Q(estado=Curso.ESTADO_PUBLICADO)
        ).distinct() # Para evitar duplicados si un curso es público y es mío
        
    def perform_create(self, serializer):
        # Asigna automáticamente al usuario logueado como el instructor del curso
        serializer.save(instructor=self.request.user)
        
        
class ModuloViewSet(viewsets.ModelViewSet):
    """ViewSet para la gestión de Módulos."""
    serializer_class = ModuloSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    # Filtrar los módulos por el curso (se accede por /cursos/{curso_ud}/modulos)
    def get_queryset(self):
        curso_pk = self.kwargs.get('curso_pk') # Obtenido de las URLs anidadas
        if curso_pk:
            return Modulo.objects.filter(curso__pk=curso_pk).order_by('orden')
        return Modulo.objects.all().order_by('orden')
    
    def perform_create(self, serializer):
        """
        Asigna automáticamente el Módulo al Curso padre (obtenido de la URL).
        """
        curso = get_object_or_404(Curso, pk=self.kwargs.get('curso_pk'))
        serializer.save(curso=curso)
    
class LeccionViewSet(viewsets.ModelViewSet):
    """ViewSet para la gestión de Lecciones."""
    serializer_class = LeccionSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    # Filtrar las lecciones por el módulo (se accede por /modulos/{modulo_id}/lecciones)
    def get_queryset(self):
        modulo_pk = self.kwargs.get('modulo_pk')
        if modulo_pk:
            return Leccion.objects.filter(modulo__pk=modulo_pk).order_by('orden')
        return Leccion.objects.all().order_by('orden')
    
    def perform_create(self, serializer):
        """
        Asigna automáticamente la Lección al Módulo padre (obtenido de la URL).
        Y dispara la tarea asíncrona si es un video.
        """
        modulo = get_object_or_404(Modulo, pk=self.kwargs.get('modulo_pk'))
        
        # Guarda la lección (aún en estado PENDIENTE)
        leccion = serializer.save(modulo=modulo)
        
        if leccion.tipo_contenido == Leccion.TIPO_VIDEO and leccion.archivo:
            leccion.estado_procesamiento = Leccion.ESTADO_PROCESANDO
            leccion.save(update_fields=['estado_procesamiento'])
            
            # Llama a la tarea asíncrona
            process_video_task.delay(leccion.id)
 
class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar y recuperar Categorías. Solo lectura
    """
    queryset = Categoria.objects.annotate(num_cursos=Count('cursos')).order_by('nombre')
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny] # Público

class CuponViewSet(viewsets.ModelViewSet):
    """
    API para que los Instructores gestionen sus propios Cupones.
    Solo pueden ver/editar/crear cupones que ellos mismos crearon.
    """
    serializer_class = CuponSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        # Un instructor solo ve sus propios cupones
        return Cupon.objects.filter(instructor=self.request.user)
    
    def perform_create(self, serializer):
        # Asigna automáticamente al instructor que lo crea
        serializer.save(instructor=self.request.user)