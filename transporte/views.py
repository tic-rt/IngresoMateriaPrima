from django.shortcuts import render

from transporte.forms import FormCamion, FormTransporte
from transporte.models import Camion, Semi, Transporte

# Create your views here.

def transportes(request):
    """Esta funcion devolvera todas las empresas de transportes registradas"""
    transportes = Transporte.objects.all()
    camiones = Camion.objects.all()
    semis = Semi.objects.all()
    form_camion = FormCamion()
    print(form_camion)
    return render(request,'transporte/transportes.html',
                  {'transportes':transportes,
                   'camiones':camiones,
                   'semis':semis,
                   'form_camion':form_camion})