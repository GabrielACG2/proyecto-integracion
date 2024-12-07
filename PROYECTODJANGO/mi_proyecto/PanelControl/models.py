from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.


class Producto(models.Model):
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
        return f"{self.nombre} ({self.categoria})"


class UsuarioManager(BaseUserManager):
    """
    Manager personalizado para el modelo Usuario que permite la creación de usuarios normales y superusuarios.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico válido.')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crear y devolver un superusuario con todos los permisos.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    """
    Modelo personalizado de usuario con campos adicionales para el registro.
    """
    username = None  # Eliminamos el campo username predeterminado de AbstractUser
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
    email = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico"
    )
    password = models.CharField(
        max_length=128,
        verbose_name="Contraseña"
    )

    # Campos adicionales para permisos
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Asignar el manager personalizado
    objects = UsuarioManager()

    # Definir el campo único para iniciar sesión
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre_completo']  # Campos requeridos además del email

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.email