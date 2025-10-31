from rest_framework import serializers
from cursos.models import Curso, Modulo, Leccion
from core.models import Usuario

# Serializer para el Instructor (para mostrar su nombre en el curso)
class InstructorSerializer(serializers.ModelSerializer):
    """Serializer minimalista para incluir los datos del instructor en el curso."""
    verificado = serializers.ReadOnlyField()
    entidad_verificada = serializers.ReadOnlyField()
    
    class Meta:
        model = Usuario
        fields = (
            'id', 'first_name', 'last_name', 'username', 'bio',
            'verificado', 'entidad_verificada'          
        )
        read_only_fields = fields # Solo lectura
        
# Lección Serializer (Nivel más interno)
class LeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leccion
        # Excluimos 'modulo' aquí para evitar la redundancia circular
        fields = ('id', 'titulo', 'orden', 'tipo_contenido', 'archivo_url', 'duracion_minutos')
    
# Módulo Serializer (Nivel intermedio: incluye lecciones)
class ModuloSerializer(serializers.ModelSerializer):
    # Serializer anidado para mostrar las lecciones dentro de cada módulo.
    lecciones = LeccionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Modulo
        fields = ('id', 'titulo', 'descripcion', 'orden', 'lecciones')
        
# Curso Detail Serializer (Vista detallada de un curso: invluye módulos)
class CursoDetailSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    # Serializer anidado para mostrar la estructura completa del curso
    modulos = ModuloSerializer(many=True, read_only=True)
    
    # Campo para obtener el nombre legible del estado
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    # Añadir campo para calcular el progreso del alumno aquí
    
    class Meta:
        model = Curso
        field = (
            'id', 'titulo', 'slug', 'descripcion', 'instructor', 'precio_usd',
            'req_certificado', 'estado', 'estado_display', 'fecha_creacion', 'fecha_actualizacion', 'modulos'
        )
        
# Curso List Serializer (Vista de listado: minimalista y rápido)
class CursoListSerializer(serializers.ModelSerializer):
    instructor_nombre = serializers.CharField(source='instructor.get_full_name', read_only=True)
    num_modulos = serializers.SerializerMethodField()
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Curso
        field = (
            'id', 'titulo', 'slug', 'descripcion', 'instructor_nombre', 
            'precio_usd', 'estado', 'estado_display', 'num_modulos'
        )
        
    # Método para calcular el número de módulos eficientemente
    def get_num_modulos(self, obj):
        return obj.modulos.count()