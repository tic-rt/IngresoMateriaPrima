from django.urls import path

from proveedores.views import agregarProducto, agregarProveedor, mostrar


urlpatterns = [
    path('mostrar',mostrar,name='mostrar'),
    path('agregarProducto', agregarProducto, name='agregarProducto'),
    path('agregarProveedor', agregarProveedor, name='agregarProveedor'),
]