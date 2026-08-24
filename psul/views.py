from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
import sweetify

from hdr.models import HDR
from psul.forms import formPsul
from porteria2.models import Ingreso
from django.db import transaction
# Create your views here.

@transaction.atomic
@login_required
@permission_required('porteria2.view_ingreso', raise_exception=True)
def pendientes(request):
    """muestra los camiones pendientes de control que provienen de IQ"""
    try:
        ingresos = Ingreso.objects.filter(ingresado = True, is_deleted = False, hdr__sector ='PSUL')
        return render(request, 'psul/pendientes.html',{'ingresos':ingresos})
    
    except Exception as excepcion:
        sweetify.error(request, 'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect ('index')

@login_required
@permission_required('porteria2.view_ingreso', raise_exception=True)
def controlPsul(request):
    """control de presion y temperatura para psul"""
    try:
        if request.method == 'GET':
            id_ingreso = request.GET.get('id_ingreso')
            ingreso = Ingreso.objects.get(id = id_ingreso, is_deleted = False , ingresado = True , hdr__estado = 'Activo', hdr__sector = 'PSUL')
            formPSUL = formPsul()
            return render (request, 'psul/control.html',{'ingreso':ingreso,'formPSUL':formPSUL})
        else:
            return redirect('pendientesPSUL')
    except Exception as excepcion:
        sweetify.error(request, 'Error', text = f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('pendientesPSUL')
    
@transaction.atomic
@login_required
@permission_required('pamo.add_pamopsul', raise_exception=True) 
def guardarPsul(request):
    try:
        if request.method == 'POST':
            id_ingreso = request.POST.get('id_ingreso')
            existe_ingreso = Ingreso.objects.filter(id = id_ingreso,ingresado = True, hdr__sector = 'PSUL', hdr__estado = 'Activo').exists()

            if existe_ingreso :
                ingreso = Ingreso.objects.get(id = id_ingreso,ingresado = True, hdr__sector = 'PSUL', hdr__estado = 'Activo')
                form_psul = formPsul(request.POST)
                form_psul.instance.hdr = ingreso.hdr
                
                if form_psul.is_valid(): 
                    hdr = HDR.objects.get(id = ingreso.hdr.id)  
                    hdr.sector =  'Almacen PQ E'
                    hdr.save()
                    form_psul.save()            
                    sweetify.success(request,'Guardado', text='Control de presion y temperatura guardados correctamente', timer=3000)
                    return redirect('pendientesPSUL')
                else:
                    sweetify.warning(request,'Error', text='Debe completar todos los campos', timer = 3000)
                    return render(request, 'psul/control.html', {'ingreso':ingreso,
                                                                 'formPSUL':form_psul})
            else:
                sweetify.error(request, 'Error', text='El ingreso referenciado no existe o fue eliminado', persistent = 'Aceptar')
                return redirect('pendientesPSUL')
            
        else:
            return redirect('pendientesPSUL')
    except Exception as excepcion:
        sweetify.error(request, 'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('pendientesPSUL')
        