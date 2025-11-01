from rest_framework import serializers
from cursos.models import Curso, Modulo, Leccion, Categoria, Etiqueta
from core.models import Usuario

# Serializer para Categoría
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Categoria
        fields = ('id', 'nombre', 'slug', 'descripcion')
        
# Serializer para Etiqueta
class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = ('id', 'nombre', 'slug')

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
    modulos = ModuloSerializer(many=True, read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    # Campos de recomendación
    categoria = CategoriaSerializer(read_only=True)
    etiquetas = EtiquetaSerializer(many=True, read_only=True)
    
    # Añadir campo para calcular el progreso del alumno aquí
    
    class Meta:
        model = Curso
        fields = (
            'id', 'titulo', 'slug', 'descripcion', 'instructor', 'precio_usd',
            'req_certificado', 'estado', 'estado_display', 'fecha_creacion', 
            'fecha_actualizacion', 'modulos', 'categoria', 'etiquetas'
        )
        
# Curso List Serializer (Vista de listado: minimalista y rápido)
class CursoListSerializer(serializers.ModelSerializer):
    instructor_nombre = serializers.CharField(source='instructor.get_full_name', read_only=True)
    num_modulos = serializers.SerializerMethodField()
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Curso
        fields = (
            'id', 'titulo', 'slug', 'descripcion', 'instructor_nombre', 
            'precio_usd', 'estado', 'estado_display', 'num_modulos'
        )
        
    # Método para calcular el número de módulos eficientemente
    def get_num_modulos(self, obj):
        return obj.modulos.count()