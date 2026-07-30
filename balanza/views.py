from datetime import datetime
from django.utils import timezone
from django.shortcuts import redirect, render
import sweetify

from balanza.forms import FormBalanza, FormBalanzaSalida
from balanza.models import Balanza
from hdr.models import HDR
from laboratorio.views import crear_inspeccion
from porteria2.models import Ingreso
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction

# Create your views here.
@login_required
@permission_required('porteria2.view_ingreso', raise_exception=True)
def balanza_index(request):
    """Funcion que devuelve la vista principal de balanza"""
    return render(request,'balanza/index.html')

@login_required
@permission_required('porteria2.view_ingreso', raise_exception=True)
def pendientes(request):
    """Funcion que devuelve todos los ingresos autorizados y que siguen a balanza"""

    try:
        ingresos = Ingreso.objects.filter(is_deleted = False, ingresado = True, hdr__sector='Almacen PQ' )
        return render(request,'balanza/pendientes.html',{'ingresos':ingresos})
    except Exception as excepcion:
        sweetify.error(request,'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('index')

@login_required
@permission_required('porteria2.view_ingreso', raise_exception=True)
def pesaje(request):
    """funcion para cargar datos de la balanza"""

    try:
        if request.method == 'GET':
            id_ingreso = request.GET.get('id_ingreso')

            existe_id = Ingreso.objects.filter(id = id_ingreso,is_deleted = False).exists()

            if existe_id:
                ingreso = Ingreso.objects.get(id = id_ingreso)
                formulario_peso = FormBalanza(initial={'remito': ingreso.remito})
                return render(request,'balanza/pesaje.html',
                              {'ingreso':ingreso,
                               'formulario_peso':formulario_peso})
            else:
                sweetify.error(request, 'Error', text='EL inreso referenciado no existe o ya fue guardado', persistent='Aceptar')
                return redirect('index')
        else:
            return redirect('index')
    except Exception as excepcion:
        sweetify.error(request, 'Error', text=f'Ocurrio un error {str(excepcion)}', persistent='Aceptar')
        return redirect('index')
    
@transaction.atomic
@login_required
@permission_required('porteria2.add_ingreso', raise_exception=True)
def guardarPesaje(request):
    try:
        if request.method == 'POST':
            formulario_pesaje = FormBalanza(request.POST)
            id_ingreso = request.GET.get('id_ingreso')
            existe_id_ingreso = Ingreso.objects.filter(id = id_ingreso).exists()

            if existe_id_ingreso and formulario_pesaje.is_valid():
                ingreso = Ingreso.objects.get(id=id_ingreso)
                hdr = Ingreso.objects.get(id = id_ingreso).hdr
                formulario_pesaje.instance.hora_ingreso = timezone.now()
                formulario_pesaje.instance.hdr = hdr
                formulario_pesaje.save()
                _definir_sector(ingreso,hdr)
                hdr.save()
                sweetify.success(request,'Guardado', text = f'Se ha guardado el pesaje para {ingreso.empresa_transporte} {ingreso.patente_chasis}', timer=3000)#faltaaa
                return redirect('pendientesBalanza')
            else:
                ingreso = Ingreso.objects.get(id=id_ingreso)
                sweetify.error(request, 'Error', text='El formulario contiene errores', persistent='Aceptar')
                return render(request, 'balanza/pesaje.html', {'formulario_peso': formulario_pesaje, 'ingreso': ingreso})
        else:
            return redirect('pendientesBalanza')
    except Exception as excepcion:
        transaction.set_rollback(True)
        sweetify.error(request,'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('pendientesBalanza')

@login_required
@permission_required('porteria2.view_ingreso',login_url='index')
def egresos(request):
    """Funcion que devuelve todos los egresos pendientes de PAMO y PSUL"""

    try:
        ingresos = Ingreso.objects.filter(is_deleted = False, ingresado = True, hdr__sector='Almacen PQ E' )
        return render(request,'balanza/egresos.html',{'ingresos':ingresos})
    except Exception as excepcion:
        sweetify.error(request,'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('index')

@login_required
@permission_required('balanza.add_balanza', raise_exception=True)
def pesajeSalida(request):
    """funcion para cargar datos de la balanza a la entrada del camion"""

    try:
        if request.method == 'GET':
            id_ingreso = request.GET.get('id_ingreso')
            existe_id = Ingreso.objects.filter(id = id_ingreso,is_deleted = False).exists()
            if existe_id:
                ingreso = Ingreso.objects.get(id = id_ingreso)
                balanza = Balanza.objects.get(hdr = ingreso.hdr.id)
                formulario_peso = FormBalanzaSalida(instance = balanza)
                return render(request,'balanza/pesaje2.html',
                              {'ingreso':ingreso,
                               'balanza':balanza,
                               'formulario_peso':formulario_peso
                               })
            else:
                sweetify.error(request, 'Error', text='EL inreso referenciado no existe o ya fue guardado', persistent='Aceptar')
                return redirect('index')
        else:
            return redirect('index')
    except Exception as excepcion:
        sweetify.error(request, 'Error', text=f'Ocurrio un error {str(excepcion)}', persistent='Aceptar')
        return redirect('index')

@transaction.atomic
@login_required
@permission_required('balanza.add_balanza', raise_exception=True)
def guardarPesaje2(request):
    """funcion para guardar datos de la balanza a la salida del camion"""
    try:
        if request.method == 'POST':
            id_ingreso = request.GET.get('id_ingreso')
            existe_id_ingreso = Ingreso.objects.filter(id = id_ingreso).exists()
            
            if existe_id_ingreso:
                ingreso = Ingreso.objects.get(id=id_ingreso)
                hdr = ingreso.hdr
                balanza = Balanza.objects.get(hdr = hdr)
                hoy = timezone.now()
                formulario_pesaje = FormBalanzaSalida(request.POST, instance = balanza)
                formulario_pesaje.instance.fecha_salida = hoy
                
                if formulario_pesaje.is_valid():
                    formulario_pesaje.save()
                    hdr.sector = 'Porteria 2 E'
                    hdr.save()
                    sweetify.success(request,'Guardado', text = f'Se ha guardado el pesaje para {ingreso.empresa_transporte} {ingreso.patente_chasis}', timer=3000)#faltaaa
                    return redirect('egresos')
                else:
                    ingreso = Ingreso.objects.get(id=id_ingreso)
                    sweetify.error(request, 'Error', text='El formulario contiene errores', persistent='Aceptar')
                    return render(request, 'balanza/pesaje2.html', {'formulario_peso': formulario_pesaje, 'ingreso': ingreso})
            else:
                sweetify.error(request, 'Error', text='El id de ingreso no existe o fue eliminado', persistent='Aceptar')
                return redirect('egresos')
        else:
            return redirect('egresos')
    except Exception as excepcion:
        transaction.set_rollback(True)
        sweetify.error(request,'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('egresos')

def _definir_sector(ingreso,hdr):
    """Funcion que define el sector de un hdr de acuerdo a si es dia laborable o no"""
    if ingreso.laborable:
        hdr.sector = 'Inspeccion PQ'
    #para dia no laborable se crea la inspeccion y se define el sector de acuerdo al producto
    else:
        match ingreso.producto.producto:
            case 'Azufre Líquido':
                hdr.sector = 'PSUL'
            case 'Azufre Sólido':
                hdr.sector = 'PSUL'
            case 'Amoníaco':
                hdr.sector = 'PAMO'
            case 'Hipoclorito':
                hdr.sector = 'PAMO'
            case _:
                hdr.sector = 'Almacen PQ E'
        #se crea la inspeccion para dia no laborable, inspeccion pq lo cerrara posteriormente
        crear_inspeccion(hdr)
        
