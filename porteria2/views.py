from datetime import date
from django.shortcuts import redirect, render
import sweetify

from hdr.models import HDR
from porteria2.forms import FormIngreso
from porteria2.models import Ingreso
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    """chart de vehiculos ingresados e informacion relevante para porteria"""
    return render(request, 'porteria2/porteria2.html')

@login_required
def nuevoIngreso(request):
    """Esta funcion devuelve un formulario de nuevo inrgeso de materia prima"""
    formulario_ingreso = FormIngreso()
    try:
        return render(request, 'porteria2/nuevoIngreso.html', {
            'formulario_ingreso': formulario_ingreso,
            # 'conductores':conductores
        })

    except Exception as excepcion:
        sweetify.error(request, title='Error', text=f'Ocurrio un error {
                       str(excepcion)}', persistent='Aceptar')
        return render(request, 'porteria2/porteria2.html')


@login_required
def guardarNuevoIngreso(request):
    """Esta funcion registra un nuevo ingreso de vehiculo a realizar descarga de materia prima y crea la hoja de ruta hdr"""
    # formulario_ingreso = FormIngreso()
    try:
        if request.method == 'POST':
            formulario = FormIngreso(request.POST)

            if formulario.is_valid():
                hdr = HDR()  # creando la hdr
                hdr.save(commit=False)
                ingreso: Ingreso = formulario.save(
                    commit=False)  # falta guardar
                ingreso.hdr = hdr
                ingreso.save()
                hdr.save()
                sweetify.success(request, title="Ingreso Guardado",
                                 text="Ingreso de vehiculo registrado", timer=3000)
                return redirect('nuevoIngreso')
            else:
                print(formulario.errors)
                errores = []
                for campo, mensajes in formulario.errors.items():
                    for mensaje in mensajes:
                        errores.append(f'{campo}: {mensaje}')

                errores_str = '<br>'.join(errores)
                sweetify.warning(request, title='Error al registrar Ingreso',
                                 text=errores_str, persistent='Aceptar')
                return render(request, 'porteria2/nuevoIngreso.html',
                              {'formulario_ingreso': formulario})

    except Exception as excepcion:
        sweetify.error(request, 'excepcion al registrar Ingreso', text=f'Ocurrio un error {
                       str(excepcion)}', persistent='Aceptar')
        return render(request, 'porteria2/nuevoIngreso.html', {'formulario_ingreso': formulario})

""" @login_required
def controlEpp(request):
     """