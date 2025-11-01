from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import Usuario

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el registro de nuevos usuarios.
    Permite registrarse como Alumno o Instructor.
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Usuario
        # Solo incluimos campos esenciales y el rol.
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'rol')
        extra_kwargs = {
            'email': {'required': True},
        }
        
    def validate_rol(self, value):
        """Valida que el rol sea Alumno o Instructor, no Administrador."""
        if value not in [Usuario.ROL_ALUMNO, Usuario.ROL_INSTRUCTOR]:
            raise serializers.ValidationError("Rol de registro no permitido.")
        return value
    
    def create(self, validate_data):
        """Crea el usuario utilizando el manager para asegurar el hash de la contraseña."""
        user = Usuario.objects.create_user(
            username=validate_data["username"],
            email=validate_data["email"],
            password=validate_data["password"],
            first_name=validate_data.get("first_name", ''),
            last_name=validate_data.get("last_name", ''),
            rol=validate_data.get('rol', Usuario.ROL_ALUMNO) # Por defecto, Alumno
        )
        return user
    
class PerfilUsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para ver y editar el perfil de usuario.
    Excluye campos sensibles como el rol y la contraseña.
    """
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)
    verificado = serializers.ReadOnlyField()
    entidad_verificada = serializers.ReadOnlyField()
    
    class Meta:
        model = Usuario
        # El campo 'bio' es crucial para los instructores
        fields = ('id', 'username', 'email', 'first_name', 
                  'last_name', 'bio', 'rol', 'rol_display', 
                  'foto_perfil', 'verificado', 'entidad_verificada'
        )
        read_only_fields = ('username', 'rol', 'email', 'verificado', 'entidad_verificada') # No se puede cambiar después del registro
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para el login (Obtener Tokens).
    Garantiza la devolución del par 'access' y 'refresh' y añade claims personalizados.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Añadimos datos extra del usuario (claims) al payload del token
        token['username'] = user.username
        token['rol'] = user.rol
        token['rol_display'] = user.get_rol_display()
        token['verificado'] = user.verificado

        return token
    
    def validate(self, attrs):
        # Llama a la validación base
        data = super().validate(attrs)
        
        return data