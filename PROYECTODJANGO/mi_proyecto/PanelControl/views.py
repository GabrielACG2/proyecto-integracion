from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Producto 
import json
from django.views.decorators.csrf import csrf_exempt


def registro_usuario(request):
    if request.method == 'POST':
        # Captura los datos del formulario
        nombre_completo = request.POST.get('fullName')
        numero_telefono = request.POST.get('phone')
        nombre_empresa = request.POST.get('company')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        acepta_terminos = request.POST.get('terms')

        # Validar contraseñas
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registroU.html')

        # Validar términos y condiciones
        if not acepta_terminos:
            messages.error(request, 'Debes aceptar los términos y condiciones.')
            return render(request, 'registroU.html')

        # Verificar si el correo ya existe
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado. Por favor, usa uno diferente.')
            return render(request, 'registroU.html')

        # Guardar datos del usuario en la base de datos
        try:
            usuario = Usuario.objects.create_user(
                email=email,
                password=password,
                nombre_completo=nombre_completo,
                numero_telefono=numero_telefono,
                nombre_empresa=nombre_empresa,
                acepta_terminos=True
            )
            usuario.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')  # Cambia 'login' por la URL de tu página de inicio de sesión
        except Exception as e:
            messages.error(request, f'Error al registrar el usuario: {str(e)}')
            return render(request, 'registroU.html')

    return render(request, 'registroU.html')


def login_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Captura el correo del formulario
        password = request.POST.get('password')  # Captura la contraseña

        # Autenticación
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirige al nombre de la vista
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')
            return render(request, 'login.html')  # Vuelve al formulario con el mensaje de error

    return render(request, 'login.html')  # Muestra el formulario en caso de GET




@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='/login/')
def inventario(request):
    return render(request, 'inventario.html')

def cerrar_sesion(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('/login/')

@login_required(login_url='/login/')
def ventas(request):
    return render(request, 'ventas.html')

@login_required(login_url='/login/')
def reportes(request):
    return render(request, 'reportes.html')



def list_inventory(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        data = [
            {
                "nombre": producto.nombre,
                "categoria": producto.categoria,
                "precio_unitario": producto.precio_unitario,  # Cambiado de 'precio' a 'precio_unitario'
                "cantidad": producto.cantidad,
                "proveedor": producto.proveedor,
                "fecha_ingreso": producto.fecha_ingreso.strftime('%Y-%m-%d')
            }
            for producto in productos
        ]
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def add_inventory(request):
    if request.method == 'POST':
        try:
            # Depura los datos enviados
            data = json.loads(request.body)
            print("Datos recibidos:", data)  # Esto imprimirá los datos en la consola del servidor

            producto = Producto.objects.create(
                nombre=data.get('nombre'),
                categoria=data.get('categoria'),
                precio_unitario=data.get('precio_unitario'),
                cantidad=data.get('cantidad'),
                proveedor=data.get('proveedor'),
                fecha_ingreso=data.get('fecha_ingreso')
            )
            return JsonResponse({"message": "Producto agregado correctamente."})
        except Exception as e:
            print("Error:", e)  # Depura el error en la consola del servidor
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Método no permitido."}, status=405)

@csrf_exempt
def modify_inventory(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            producto = Producto.objects.get(nombre=data['nombre'])
            producto.categoria = data['categoria']
            producto.precio = data['precio']
            producto.cantidad = data['cantidad']
            producto.proveedor = data['proveedor']
            producto.fecha = data['fecha']
            producto.save()
            return JsonResponse({"message": "Producto modificado correctamente."})
        except Producto.DoesNotExist:
            return JsonResponse({"error": "Producto no encontrado."}, status=404)
    return JsonResponse({"error": "Método no permitido."}, status=405)

@csrf_exempt
def delete_inventory(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            producto = Producto.objects.get(nombre=data['nombre'])
            producto.delete()
            return JsonResponse({"message": "Producto eliminado correctamente."})
        except Producto.DoesNotExist:
            return JsonResponse({"error": "Producto no encontrado."}, status=404)
    return JsonResponse({"error": "Método no permitido."}, status=405)

from .models import Producto

def search_inventory(request):
    field = request.GET.get('field')
    value = request.GET.get('value')

    if field not in ['nombre', 'categoria', 'proveedor']:
        return JsonResponse({'error': 'Campo no válido'}, status=400)

    filters = {f'{field}__icontains': value}
    productos = Producto.objects.filter(**filters)

    data = list(productos.values('nombre', 'categoria', 'precio_unitario', 'cantidad', 'proveedor', 'fecha_ingreso'))
    return JsonResponse(data, safe=False)

