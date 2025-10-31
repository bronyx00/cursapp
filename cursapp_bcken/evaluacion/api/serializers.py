from rest_framework import serializers
from evaluacion.models import Inscripcion
from cursos.models import Curso

class InscripcionSerializer(serializers.ModelSerializer):
    """
    Serializer para crear una nueva inscripción (Iniciar un proceso de pago)
    """
    curso_titulo = serializers.ReadOnlyField(source='curso.titulo')
    
    class Meta:
        model = Inscripcion
        field = (
            'id', 'curso', 'curso_titulo', 'alumno',
            'precio_pagado_usd', 'estado_pago', 'referencia_pago',
            'fecha_inscripcion'
        )
        read_only_fields = ('alumno', 'precio_pagado_usd', 'estado_pago', 'referencia_pago')
        
class InscripcionCrearSerializer(serializers.ModelSerializer):
    """
    Serializer simplicado solo para la creación.
    El alumno solo necesita enviar el ID del curso.
    """
    class Meta:
        model = Inscripcion
        fields = ('curso',)
        
    def create(self, validated_data):
        # La lógica de creación se moverá al ViewSet para obtener el usuario y el precio.
        return super().create(validated_data)
    
class LeaderboardSerializer(serializers.Serializer):
    """
    Serializer especial para la tabla de calificación (Leaderboard).
    Usa campos basados en la agregación de la base de datos.
    """
    alumno_id = serializers.IntegerField(source='alumno')
    username = serializers.CharField(source='alumno__username')
    full_name = serializers.SerializerMethodField()
    puntuacion_total = serializers.IntegerField(source='puntos_totales')
    
    def get_full_name(self, obj):
        return f"{obj['alumno__first_name']} {obj['alumno__last_name']}"