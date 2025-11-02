from rest_framework_nested import routers
from .viewsets import PreguntaForoViewSet, RespuestaForoViewSet

# NO usamos un router base, yaque este módulo se anidará desde 'cursos'

# Ruta: .../lecciones/{leccion_pk}/preguntas/
preguntas_router = routers.SimpleRouter()
preguntas_router.register(r'preguntas', PreguntaForoViewSet, basename='leccion-preguntas')

# Ruta: .../preguntas/{pregunta_pk}/respuestas/
respuestas_router = routers.NestedSimpleRouter(preguntas_router, r'preguntas', lookup='pregunta')
respuestas_router.register(r'respuestas', RespuestaForoViewSet, basename='pregunta-respuesta')

urlpatterns = preguntas_router.urls + respuestas_router.urls