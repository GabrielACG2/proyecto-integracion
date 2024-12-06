from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_unitario', 'cantidad', 'proveedor', 'fecha_ingreso')
    search_fields = ('nombre', 'categoria', 'proveedor')
