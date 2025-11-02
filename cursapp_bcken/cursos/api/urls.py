from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .viewsets import CursoViewSet, ModuloViewSet, LeccionViewSet
from evaluacion.api.viewsets import ResenaViewSet
from comunidad.api.viewsets import PreguntaForoViewSet, RespuestaForoViewSet

# Router Principal para el Curso
router = DefaultRouter()
router.register(r'catalogo', CursoViewSet, basename='curso-catalogo')

# Router Anidado para Módulos (curso/{pk}/modulos/)
cursos_router = routers.NestedSimpleRouter(router, r'catalogo', lookup='curso')
cursos_router.register(r'modulos', ModuloViewSet, basename='curso-modulos')

# Router Anidado para Lecciones (curso/1/modulos/2/lecciones/)
modulos_router = routers.NestedSimpleRouter(cursos_router, r'modulos', lookup='modulo')
modulos_router.register(r'lecciones', LeccionViewSet, basename='modulo-lecciones')

# Router Anidado desde lecciones par el foro
preguntas_router = routers.NestedSimpleRouter(modulos_router, r'lecciones', lookup='leccion')
preguntas_router.register(r'preguntas', PreguntaForoViewSet,  basename='leccion-prerguntas')

# Router Anidado desde preguntas para las respuestas
respuestas_router = routers.NestedSimpleRouter(preguntas_router, r'preguntas', lookup='pregunta')
respuestas_router.register(r'respuestas', RespuestaForoViewSet, basename='pregunta-respuestas')

# Router Anidado para Reseñas (cursos/{curso_pk}/resenas/)
resenas_router = routers.NestedSimpleRouter(router, r'catalogo', lookup='curso')
resenas_router.register(r'resenas', ResenaViewSet, basename='curso-resenas')

urlpatterns = router.urls + cursos_router.urls + modulos_router.urls + resenas_router.urls + preguntas_router.urls + respuestas_router.urls