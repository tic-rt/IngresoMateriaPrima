from django.shortcuts import render

from porteria2.models import Ingreso

# Create your views here.

def lista_hdr(request):
    """Funcion que devuelve la vista principal de hdr"""
    hdr = None
    try:
        hdr = Ingreso.objects.filter(ingresado = True)
    except Exception as excepcion:
        pass
    
    return render(request,'HDR/listaHDR.html',{'HDR':hdr})

def exportar_hdr(request):
    """Funcion que exporta la lista de hdr a pdf"""
    return render(request,'HDR/HDR.html')