from django.urls import path
from .views import registro_usuario, login_usuario, index, cerrar_sesion, inventario, ventas, reportes  # Importa tu vista de registro
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from .views import list_inventory, add_inventory, modify_inventory, delete_inventory, search_inventory

urlpatterns = [
    path('registro/', registro_usuario, name='registro'),
    path('', lambda request: redirect(reverse('login'))),
    path('login/', login_usuario, name='login'),  # Cambia a tu vista personalizada
    path('index/', index, name='index'),
    path('cerrar-sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('inventario/', inventario, name='inventario'),
    path('ventas/', ventas, name='ventas'),
    path('reportes/', reportes, name='reportes'),
    
    path('inventario/list/', list_inventory, name='list_inventory'),
    path('inventario/add/', add_inventory, name='add_inventory'),
    path('inventario/modify/', modify_inventory, name='modify_inventory'),
    path('inventario/delete/', delete_inventory, name='delete_inventory'),
    path('inventario/search/', search_inventory, name='search_inventory')
]