from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Producto(models.Model):
    """
    Modelo para representar los productos en el inventario.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre del producto")
    categoria = models.CharField(max_length=50, verbose_name="Categoría")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad en stock")
    proveedor = models.CharField(max_length=100, verbose_name="Proveedor")
    fecha_ingreso = models.DateField(verbose_name="Fecha de ingreso al inventario")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    """
    Modelo personalizado de usuario con campos adicionales para el registro,
    incluyendo contraseña, nombre completo, y otros campos del formulario.
    """

    # Campos adicionales
    nombre_completo = models.CharField(
        max_length=100,
        verbose_name="Nombre completo"
    )
    numero_telefono = models.CharField(
        max_length=15,
        verbose_name="Número de teléfono"
    )
    nombre_empresa = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Nombre de la empresa"
    )
    acepta_terminos = models.BooleanField(
        default=False,
        verbose_name="Acepta los términos y condiciones"
    )

    # Sobrescritura de email
    email = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico"
    )

    # Campo de contraseña (ya está incluido en AbstractUser, pero lo mencionamos explícitamente)
    password = models.CharField(
        max_length=128,
        verbose_name="Contraseña"
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username