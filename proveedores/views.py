from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import sweetify

from proveedores.models import Producto, Proveedor

# Create your views here.

@login_required
def mostrar(request):
    """devuelve una lista de proveedores y productos"""

    try:
        if request.method == 'GET':
            proveedores = Proveedor.objects.filter(is_deleted = False)
            productos = Producto.objects.filter(is_deleted = False)
            return render(request, 'proveedor/proveedor.html',
                          {'proveedores':proveedores,
                           'productos':productos})
        else:
            return redirect('mostrar')
    except Exception as exepcion:
        sweetify.error(request, 'Error', text=f'Ocurrio un error{str(exepcion)}', persistent = 'Aceptar')
        return redirect('index')
    
@login_required
def agregarProveedor(request):
    """Agrega un nuevo Proveedor"""
    try:
        if request.method == 'POST':
            nombre_proveedor:str = request.POST.get('proveedor')
            nombre_proveedor = nombre_proveedor.title()
            proveedor = Proveedor(nombre=nombre_proveedor)
            proveedor.save()
            print(nombre_proveedor)
            sweetify.success(request, 'Guardado', text =f'Se guardo al proveedor {nombre_proveedor}', timer = 3000)
            return redirect('mostrar')
    except Exception as excepcion:
        sweetify.error(request, 'Error', text =f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('mostrar')
    
@login_required
def agregarProducto(request):
    """Agrega un nuevo Producto"""
    try:
        if request.method == 'POST':
            nombre_producto:str = request.POST.get('producto')
            nombre_producto = nombre_producto.title()
            producto = Producto(nombre=nombre_producto)
            producto.save()
            sweetify.success(request, 'Guardado', text =f'Se guardo al producto {nombre_producto}', timer = 3000)
            return redirect('mostrar')
    except Exception as excepcion:
        sweetify.error(request, 'Error', text =f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('mostrar')