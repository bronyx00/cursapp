from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración para el modelo de Usuario personalizado en el Admin.
    """
    # Campos que se mostrarán en la lista de usuarios
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'rol',
        'verificado',
        'is_staff',
        'xp_totales'
    )
    
    # Filtros laterales
    list_filter = ('rol', 'verificado', 'is_staff', 'is_active', 'groups')
    
    # Campos de búsqueda
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Campos editables en el formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Roles y Verificación', {
            'fields': ('rol', 'verificado', 'entidad_verificada'),
        }),
        ('Datos del Marketplace', {
            'fields': ('comision', 'bio', 'foto_perfil'),
        }),
        ('Gamificación (Solo lectura)', {
            'fields': ('puntos_totales', 'xp_totales'),
        }),
    )
    
    # Los campos de gamificación son solo de lectura en el admin
    readonly_fields = ('puntos_totales', 'xp_totales', 'date_joined', 'last_login')