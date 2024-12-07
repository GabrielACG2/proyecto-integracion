from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Producto  # Importa tus modelos

class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'nombre_completo', 'numero_telefono', 'is_active', 'is_staff')
    search_fields = ('email', 'nombre_completo', 'numero_telefono')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nombre_completo', 'numero_telefono', 'nombre_empresa')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'nombre_completo', 'numero_telefono', 'nombre_empresa', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(Usuario, UsuarioAdmin)

# Registrar el modelo Producto (si aplica)
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_unitario', 'cantidad', 'proveedor', 'fecha_ingreso')
    search_fields = ('nombre', 'categoria', 'proveedor')
