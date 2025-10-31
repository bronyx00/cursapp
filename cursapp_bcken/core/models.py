from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Usuario(AbstractUser):
    """
    Modelo de Usuario Personalizado para gestionar Roles. 
    Extiende el AbstractUser de Django para añadir un campo de rol y otras propiedades específicas.
    """
    # Constantes para definir los roles
    ROL_ADMIN = 1
    ROL_INSTRUCTOR = 2
    ROL_ALUMNO = 3
    
    ROLES_CHOICES = (
        (ROL_ADMIN, 'Administrador'),
        (ROL_INSTRUCTOR, 'Profesor'),
        (ROL_ALUMNO, 'Alumno'),
    )
    
    verificado = models.BooleanField(
        default=False,
        help_text="Indica si la cuenta ha sido verificada oficialmente por la plataforma."
    )
    
    entidad_verificada = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nombre de la Universidad/Organización si aplica."
    )
    
    rol = models.PositiveSmallIntegerField(
        choices=ROLES_CHOICES, 
        default=ROL_ALUMNO, 
        verbose_name='Rol de Usuario'
    )
    
    # Campos adicionales
    bio = models.TextField(max_length=500, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    
    # Campo para almacenar la comisión. (ej. 15%)
    comision = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=15.00,
        verbose_name='Comisión de la Plataforma (%)'
    )
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.get_rol_display()}: {self.username}"
    
    # Métodos de utilidad para permisos
    @property
    def es_admin(self):
        return self.rol == self.ROL_ADMIN
    
    @property
    def es_instructor(self):
        """Método helper para verificar si es profesor."""
        return self.rol == self.ROL_INSTRUCTOR
    
    @property
    def es_alumno(self):
        """Método helper para verificar si es alumno."""
        return self.rol == self.ROL_ALUMNO
    