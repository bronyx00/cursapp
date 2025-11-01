from rest_framework import serializers
from evaluacion.models import Inscripcion, ProgresoLeccion
from core.models import Usuario

class InscripcionSerializer(serializers.ModelSerializer):
    """
    Serializer para crear una nueva inscripción (Iniciar un proceso de pago)
    """
    curso_titulo = serializers.ReadOnlyField(source='curso.titulo')
    
    class Meta:
        model = Inscripcion
        fields = (
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
    
class LeaderboardSerializer(serializers.ModelSerializer):
    """
    Serializer especial para la tabla de calificación (Leaderboard).
    Usa el modelo Usuario.
    """
    full_name = serializers.CharField(source='get_full_name')
    puntuacion_total = serializers.IntegerField(source='xp_totales') # Usamos XP para el Leaderboard
    
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'full_name', 'puntuacion_total', 'foto_perfil')
        
class ScormProgresoSerializer(serializers.ModelSerializer):
    """
    Serializer específico para la comunicación SCORM.
    Maneja los campos CMI (Computer-Managed Instruction) que guardamos
    en el modelo ProgresoLeccion
    """
    class Meta:
        model = ProgresoLeccion
        
        # Campos que se podrán LEER y ACTUALIZAR desde Vue.js
        fields = (
            'id',
            'leccion',
            'estado_scorm', # (Ej: 'completed', 'failed', 'incomplete') 
            'puntuacion_scorm', # (Ej: 80.5)
            'suspend_data', # (Ej: "pagina_3, pregunta_5")
            'entry_point', # (Ej: 'resume' o 'ab-inition')
            'completado'
        )
        read_only_fields = ('id', 'leccion')