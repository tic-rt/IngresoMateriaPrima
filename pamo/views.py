from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import sweetify

from hdr.models import HDR
from pamo.forms import formPamo
from porteria2.models import Ingreso
from django.contrib.auth.decorators import permission_required
from django.db import transaction

# Create your views here.
@transaction.atomic 
@login_required
@permission_required('pamo.view_pamo', raise_exception=True)
def pendientes(request):
    """muestra los camiones pendientes de control que provienen de IQ"""
    try:
        ingresos = Ingreso.objects.filter(ingresado = True, is_deleted = False, hdr__sector ='PAMO')
        return render(request, 'pamo/pendientes.html',{'ingresos':ingresos})
    
    except Exception as excepcion:
        sweetify.error(request, 'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect ('index')
    
@transaction.atomic    
@login_required
@permission_required('pamo.add_pamo', raise_exception=True)
def controlPamo(request):
    """control de presion y temperatura para pamo"""
    try:
        if request.method == 'GET':
            id_ingreso = request.GET.get('id_ingreso')
            ingreso = Ingreso.objects.get(id = id_ingreso, is_deleted = False , ingresado = True , hdr__estado = 'Activo', hdr__sector = 'PAMO')
            formPAMO = formPamo()
            return render (request, 'pamo/control.html',{'ingreso':ingreso,'formPAMO':formPAMO})
        else:
            return redirect('pendientesPAMO')
    except Exception as excepcion:
        sweetify.error(request, 'Error', text = f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('pendientesPAMO')
@transaction.atomic
@login_required
@permission_required('pamo.add_pamo', raise_exception=True) 
def guardarPamo(request):
    try:
        if request.method == 'POST':
            id_ingreso = request.POST.get('id_ingreso')
            existe_ingreso = Ingreso.objects.filter(id = id_ingreso,ingresado = True, hdr__sector = 'PAMO', hdr__estado = 'Activo').exists()

            if existe_ingreso :
                ingreso = Ingreso.objects.get(id = id_ingreso,ingresado = True, hdr__sector = 'PAMO', hdr__estado = 'Activo')
                form_pamo = formPamo(request.POST)
                form_pamo.instance.hdr = ingreso.hdr
                
                if form_pamo.is_valid(): 
                    hdr = HDR.objects.get(id = ingreso.hdr.id)  
                    hdr.sector =  'Almacen PQ E'
                    hdr.save()
                    form_pamo.save()            
                    sweetify.success(request,'Guardado', text='Control de presion y temperatura guardados correctamente', timer=3000)
                    return redirect('pendientesPAMO')
                else:
                    sweetify.warning(request,'Error', text='Debe completar todos los campos', timer = 3000)
                    return render(request, 'pamo/control.html', {'ingreso':ingreso,
                                                                 'formPAMO':form_pamo})
            else:
                sweetify.error(request, 'Error', text='El ingreso referenciado no existe o fue eliminado', persistent = 'Aceptar')
                return redirect('pendientesPAMO')
            
        else:
            return redirect('pendientesPAMO')
    except Exception as excepcion:
        sweetify.error(request, 'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('pendientesPAMO')
        