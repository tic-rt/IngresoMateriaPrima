from django.http import HttpResponse
from django.shortcuts import redirect, render

from transporte.forms import FormCamion, FormTransporte
from transporte.models import Camion, Semi, Transporte
import sweetify

# Create your views here.

def transportes(request):
    """Esta funcion devolvera todas las empresas de transportes registradas"""
    transportes = Transporte.objects.all()
    camiones = Camion.objects.all()
    semis = Semi.objects.all()
    form_transporte = FormTransporte()
    form_camion = FormCamion()
    return render(request,'transporte/transportes.html',
                  {'transportes':transportes,
                   'camiones':camiones,
                   'semis':semis,
                   'form_transporte': form_transporte,
                   'form_camion':form_camion})

def agregarTransporte(request):
    """esta funcion agrega una empresa de trasnporte nueva"""
    try:
        if request.method == 'POST':
            transporte = FormTransporte(request.POST)
            if(transporte.is_valid()):
                 transporte.save()
                 sweetify.toast(request,f'Empresa de transporte {transporte.cleaned_data['nombre']} agregada',icon='success',timer = 5000)
                 return redirect('transportes')
            else:
                print(transporte.errors)
                sweetify.warning(request,'Error al agregar  empresa de transporte', text='Verifica si la empresa ya existe', persistent = 'Aceptar')
                return redirect('transportes')
    except Exception as error :
            sweetify.error('Error al agregar Empresa de transporte', persistent=f'ocurrio un error {str(error)}')
            return redirect('transportes')
    
        