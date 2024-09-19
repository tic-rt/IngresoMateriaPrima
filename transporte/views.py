from django.http import HttpResponse
from django.shortcuts import redirect, render

from transporte.forms import FormCamion, FormTransporte, formSemi
from transporte.models import Camion, Semi, Transporte
import sweetify

# Create your views here.

def transportes(request):
    """Esta funcion devolvera todas las empresas de transportes registradas ,camiones y semis
        junto a los formularios correspondientes para la carga"""
    transportes = Transporte.objects.all()
    camiones = Camion.objects.all()
    semis = Semi.objects.all()
    form_transporte = FormTransporte()
    form_camion = FormCamion()
    form_semi = formSemi()
    return render(request,'transporte/transportes.html',
                  
                  {'transportes':transportes,
                   'camiones':camiones,
                   'semis':semis,
                   'form_transporte': form_transporte,
                   'form_camion':form_camion,
                   'form_semi':form_semi
                   })

def agregarTransporte(request):
    """esta funcion agrega una empresa de transporte nueva"""
    try:
        if request.method == 'POST':
            transporte = FormTransporte(request.POST)
            
            if(transporte.is_valid()):
                 transporte.save()
                 sweetify.toast(request,f'Empresa de transporte {transporte.clean_nombre()} agregada',icon='success',timer = 5000)
                 return redirect('transportes')
            else:
                errores = []
                for campo, mensajes in transporte.errors.items():
                    for mensaje in mensajes:
                        errores.append(f'{campo}: {mensaje}')
                
                errores_str = '<br>'.join(errores)
                sweetify.warning(request,'Error al agregar empresa de transporte', text = errores_str, persistent = 'Aceptar')
                return redirect('transportes')
    except Exception as excepcion :
        sweetify.error('Error al agregar Empresa de transporte', persistent=f'ocurrio un error {str(excepcion)}')
        return redirect('transportes')
    
def agregarCamion(request):
    """Esta funcion agrega un nuevo camion"""
    try:
        if request.method == 'POST':
            camion = FormCamion(request.POST)
            if(camion.is_valid()):
                camion.save()
                sweetify.toast(request,f'Camion patente {camion.clean_patente()} agregado', icon='success', timer=5000)
                return redirect('transportes')
            else:
                errores = []
                for campo, mensajes in camion.errors.items():
                    for mensaje in mensajes:
                        errores.append(f'{campo}: {mensaje}')
                
                errores_str = '<br>'.join(errores)
                sweetify.warning(request,'Error al agregar empresa de transporte', text = errores_str, persistent = 'Aceptar')
                return redirect('transportes')
    except Exception as excepcion:
        sweetify.error(request,'Error al agregar camion',persistent=f'ocurrio un error {str(excepcion)}')
        return redirect('transportes')
            