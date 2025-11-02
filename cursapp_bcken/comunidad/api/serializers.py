from rest_framework import serializers
from core.api.serializers import PerfilUsuarioSerializer
from comunidad.models import PreguntaForo, RespuestaForo

class RespuestaForoSerializer(serializers.ModelSerializer):
    autor = PerfilUsuarioSerializer(read_only=True)
    
    class Meta:
        model = RespuestaForo
        fields = ('id', 'pregunta', 'autor', 'cuerpo', 'es_util', 'fecha_creacion')
        read_only_fields = ('pregunta', 'autor')
    
class PreguntaForoSerializer(serializers.ModelSerializer):
    autor = PerfilUsuarioSerializer(read_only=True)
    # Mostramos las respuestas anidadas
    respuestas = RespuestaForoSerializer(many=True, read_only=True)
    
    class Meta:
        model = PreguntaForo
        fields = ('id', 'leccion', 'autor', 'titulo', 'cuerpo', 'fecha_creacion', 'respuestas')
        read_only_fields = ('leccion', 'autor')