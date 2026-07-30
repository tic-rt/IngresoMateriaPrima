
from django.shortcuts import redirect, render
import sweetify

from hdr.models import HDR
from laboratorio.forms import FormLaboratorio
from laboratorio.models import Inspeccion
from personal.models import Personal
from porteria2.models import Ingreso
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction

# Create your views here.
@login_required
@permission_required('porteria2.view_ingreso', raise_exception=True)
def pendientes(request):
    """muestra los camiones pendientes de control despues que pasaron por balanza"""
    try:
        ingresos = Ingreso.objects.filter(ingresado = True, is_deleted = False,hdr__sector='Inspeccion PQ')
        return render (request, 'laboratorio/pendientes.html',{'ingresos':ingresos})
    except Exception as excepcion:
        sweetify.error(request, 'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect ('index')
    
def pendientes_control(request):
    """muestra los camiones pendientes de control en dias no laborables"""
    try:
        #la consulta trae todos los ingresos con dias no laborables y inspeccion en estado cerrado = False
        ingresos = Ingreso.objects.filter(ingresado = True,is_deleted = False,laborable = False,hdr__inspeccion__cerrado = False)
        return render(request, 'laboratorio/control_pendiente.html',{'ingresos':ingresos})
    except Exception as excepcion:
        sweetify.error(request, 'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect ('index')
        
    
@login_required
@permission_required('porteria2.view_ingreso', raise_exception=True)
def inspeccion(request):
    """Esta funcion devuelve el formulario de control de inspeccion quimica"""
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
    
def inspeccion_pendiente(request):
    """Esta funcion devuelve el formulario de control de inspeccion quimica pendiente correspondiente a un dia no laborable"""
    try:
        if request.method == 'GET':
            id_ingreso = request.GET.get('id_ingreso')
            id_hdr = request.GET.get('id_hdr')
            
            if __controlIds(id_ingreso, id_hdr):
                ingreso = Ingreso.objects.get(id = id_ingreso, is_deleted = False, hdr_id = id_hdr)
                inspeccion = Inspeccion.objects.get(hdr = id_hdr)
                formulario_inspeccion = FormLaboratorio(instance = inspeccion)
                return render(request,'laboratorio/guardar_control_pendiente.html',{'ingreso':ingreso, 'formulario_inspeccion':formulario_inspeccion})

            else:
                sweetify.error(request,'Error', text=f'El id de ingreso o hdr referenciados no existen o fueron eliminados', persistent = 'Aceptar')
                return redirect('inspeccion_pendiente')
            
        else:
            return redirect('index')
    except Exception as excepcion:
        sweetify.error(request, 'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('pendientesInspeccion')
    

@transaction.atomic
@login_required
@permission_required('laboratorio.add_inspeccion', raise_exception=True)
def guardar_inspeccion(request):
    """Esta funcion guarda un control de inspeccion quimica """
    try:
        if request.method == 'POST':
            id_ingreso = request.POST.get('id_ingreso')
            id_hdr = request.POST.get('id_hdr')
            formulario_control = FormLaboratorio(request.POST)
            if __controlIds(id_ingreso, id_hdr):
                ingreso = Ingreso.objects.get(id = id_ingreso, is_deleted = False, hdr_id = id_hdr)
                hdr = ingreso.hdr
                
                if formulario_control.is_valid():
                    #Si es amoniaco o azufre liquido debo guardar y  enviarlo a control de PAMPO\PSUL
                    if ingreso.producto.producto == 'Azufre Líquido':
                        hdr.sector = 'PSUL'
                    elif ingreso.producto.producto == 'Azufre Sólido':
                        hdr.sector = 'PSUL'
                    elif ingreso.producto.producto == 'Hipoclorito':
                        hdr.sector = 'PAMO'
                    elif ingreso.producto.producto == 'Amoníaco':
                        hdr.sector = 'PAMO'
                    else:
                        hdr.sector = 'Almacen PQ E'

                    hdr.save(update_fields=['sector'])
                    inspeccion = formulario_control.save(commit=False)
                    inspeccion.cerrado = True
                    inspeccion.hdr = hdr
                    inspeccion.save()
                    
                    sweetify.success(request, 'Guardado', text=f'Control de Inspección de {ingreso.producto} guardado', timer=3000)
                    return redirect('pendientesInspeccion')
                        
                else:
                    return render(request, 'laboratorio/control.html',{'ingreso':ingreso,'formulario_inspeccion':formulario_control})
                
            else:
                sweetify.error(request, 'Error', text = 'El id de Ingreso o de HDR referenciados no existen o fueron borrados', persistent = 'Aceptar')
                return redirect('pendientesInspeccion')
            
    except Exception as excepcion:
        transaction.set_rollback(True)
        sweetify.error(request, 'Error', text=f'Ocurrió un error: {str(excepcion)}', persistent='Aceptar')
        return redirect('pendientesInspeccion')

@transaction.atomic
@login_required
@permission_required('laboratorio.add_inspeccion', raise_exception=True)
def guardar_inspeccion_pendiente(request):
    """Esta funcion guarda un control de inspeccion quimica pendiente  correspondiente a un dia no laborable """
    
    try:
        if request.method == 'POST':
            id_ingreso = request.POST.get('id_ingreso')
            id_hdr = request.POST.get('id_hdr')
            if __controlIds(id_ingreso, id_hdr):
                ingreso = Ingreso.objects.get(id = id_ingreso, is_deleted = False, hdr_id = id_hdr)
                inspeccion = Inspeccion.objects.get(hdr = id_hdr)
                formulario_control = FormLaboratorio(request.POST, instance=inspeccion)
                if formulario_control.is_valid():
                    
                    inspeccion = formulario_control.save(commit=False)
                    inspeccion.cerrado = True
                    inspeccion.save()
                    
                    sweetify.success(request, 'Guardado', text=f'Control de Inspección Pendiente de {ingreso.producto} guardado', timer=3000)
                    return redirect('pendientesInspeccion')
                        
                else:
                    return render(request, 'laboratorio/control.html',{'ingreso':ingreso,'formulario_inspeccion':formulario_control})
                
            else:
                sweetify.error(request, 'Error', text = 'El id de Ingreso o de HDR referenciados no existen o fueron borrados', persistent = 'Aceptar')
                return redirect('pendientesInspeccion')
            
    except Exception as excepcion:
        transaction.set_rollback(True)
        sweetify.error(request, 'Error', text=f'Ocurrió un error: {str(excepcion)}', persistent='Aceptar')
        return redirect('pendientesInspeccion')



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
    
def crear_inspeccion(hdr):
    """Esta funcion crea una instancia de inspeccion para posterior control"""
    personal_sin_asignar, _ = Personal.objects.get_or_create(
        legajo='--',
        defaults={
            'sector': 'Inspeccion Quimica',
            'nombre': 'Sin',
            'apellido': 'Asignar',
            'is_deleted': False
        }
    )
    inspeccion = Inspeccion.objects.create(  
        certificado = False,
        requisitos = False,
        descargar = False,
        responsable = personal_sin_asignar,
        observacion = '',
        cerrado = False,
        hdr = hdr,
        )   
    inspeccion.save()         
