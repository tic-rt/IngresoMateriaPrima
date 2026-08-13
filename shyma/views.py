from django.http import request
import sweetify

from django.shortcuts import redirect, render
from porteria2.models import Ingreso
from porteria2.forms import FormIngreso
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction

# Create your views here.
@login_required
@permission_required('porteria2.view_ingreso', raise_exception=True)
def mostrar_en_transito(request):
    """Esta funcion devuelve una lista de camiones en transito"""
    try:
        ingresos = Ingreso.objects.filter(ingresado = True, is_deleted = False, hdr__estado = 'Activo')
        print(ingresos)
        return render(request,'shyma/transito.html',{'ingresos':ingresos})
    except Exception as excepcion:
        sweetify.error(request, 'Error', text=f'Ocurrio un error al mostrar la lista {str(excepcion)}', persistent = 'Aceptar')
        return redirect('index')

@login_required
@permission_required('porteria2.view_ingreso', raise_exception=True)
def cargar_en_transito(request):
    """Esta funcion carga un ingreso y la hdr para su rechazo"""
    sweetify.warning(request, 'Advertencia', text= 'Esta a punto de rechazar una HDR,no se podá deshacer el rechazo', persistent = 'Aceptar')
    try:
        if request.method == 'GET' :
            id_ingreso = request.GET.get('id_ingreso')
            id_hdr = request.GET.get('id_hdr')
            ingreso = Ingreso.objects.get(id = id_ingreso)
            hdr = ingreso.hdr

            formulario_ingreso = FormIngreso(instance = ingreso)
            for field in formulario_ingreso.fields.values():
                field.disabled = True
                formulario_ingreso.helper.inputs = []
                
            return render(request,'shyma/rechazo.html',{'ingreso':ingreso,'formulario_ingreso':formulario_ingreso,'id_ingreso':id_ingreso,'id_hdr':id_hdr})

    except Exception as excepcion:
        sweetify.error(request,'Error', text = f'Ha ocurrido un error {str(excepcion)}', persistent = 'Aceptar' )
        return redirect('index')
    
@login_required
@permission_required('porteria2.change_hdr', raise_exception=True)
@transaction.atomic
def guardar_rechazo(request):
    """Esta funcion guarda un rechazo por parte de SHYMA, actualizando el estado de la HDR a Rechazado y guardando la observacion"""
    try:
        if request.method == 'POST':
                id_ingreso = request.POST.get('id_ingreso')
                observacion = request.POST.get('observacion', '').strip()
                ingreso = Ingreso.objects.get(id = id_ingreso)
                hdr = ingreso.hdr
                hdr.estado = 'Rechazado'
                if observacion:
                    if hdr.observacion:
                        hdr.observacion = f"{hdr.observacion}\n{observacion}"[:200]
                    else:
                        hdr.observacion = observacion[:200]
                hdr.save()
                sweetify.success(request, 'Exito', text= 'Se ha rechazado la HDR correctamente', persistent = 'Aceptar')
                return redirect('en_transito')
    except Exception as excepcion:
        sweetify.error(request, 'Error', text= f'Ocurrio un error al rechazar la HDR {str(excepcion)}', persistent = 'Aceptar')
        return redirect('en_transito')
