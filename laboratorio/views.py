from django.shortcuts import redirect, render
import sweetify

from hdr.models import HDR
from laboratorio.forms import FormLaboratorio
from porteria2.models import Ingreso

# Create your views here.

def pendientes(request):
    """muestra los camiones pendientes de control despues que pasaron"""
    try:
        ingresos = Ingreso.objects.filter(ingresado = True, is_deleted = False,hdr__sector='Inspeccion PQ')
        return render (request, 'laboratorio/pendientes.html',{'ingresos':ingresos})
    except Exception as excepcion:
        sweetify.error(request, 'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect ('index')

def inspeccion(request):
    try:
        if request.method == 'GET':
            id_ingreso = request.GET.get('id_ingreso')
            id_hdr = request.GET.get('id_hdr')
            
            if __controlIds(id_ingreso, id_hdr):
                ingreso = Ingreso.objects.get(id = id_ingreso, is_deleted = False, hdr_id = id_hdr)
                formulario_inspeccion = FormLaboratorio()
                return render(request,'laboratorio/control.html',{'ingreso':ingreso, 'formulario_inspeccion':formulario_inspeccion})

            else:
                sweetify.error(request,'Error', text=f'El id de ingreso o hdr referenciados no existen o fueron eliminados', persistent = 'Aceptar')
                return redirect('pendientesInspeccion')
            
        else:
            return redirect('index')
    except Exception as excepcion:
        sweetify.error(request, 'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('pendientesInspeccion')

def guardarInspeccion(request):
    """Esta funcion guarda un control de inspeccion quimica """
    try:
        if request.method == 'POST':
            id_ingreso = request.POST.get('id_ingreso')
            id_hdr = request.POST.get('id_hdr')
            formulario_control = FormLaboratorio(request.POST)
            
            if __controlIds(id_ingreso, id_hdr):
                ingreso = Ingreso.objects.get(id = id_ingreso, is_deleted = False, hdr_id = id_hdr)
                
                if formulario_control.is_valid():
                    pass
                else:
                    return render(request, 'laboratorio/control.html',{'ingreso':ingreso,'formulario_inspeccion':formulario_control})

    except Exception as excepcion:
        pass

def __controlIds(id_ingreso, id_hdr):
    """Controla si un id de ingreso y un id de hdr existen al mismo tiempo """
    
    id_ingreso = id_ingreso
    id_hdr = id_hdr
    existe_ingreso = Ingreso.objects.filter(is_deleted = False, id = id_ingreso).exists()
    existe_hdr = HDR.objects.filter(is_deleted = False, id = id_hdr).exists()

    if existe_ingreso and existe_hdr:
        return True
    else:
        return False
    