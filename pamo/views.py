from django.shortcuts import redirect, render
import sweetify

from porteria2.models import Ingreso

# Create your views here.
def pendientes(request):
    """muestra los camiones pendientes de control que provienen de IQ"""
    try:
        ingresos = Ingreso.objects.filter(ingresado = True, is_deleted = False, hdr_sector ='PAMO/PSUL' )
        return render('pamo/pendientes.html',{'ingresos':ingresos})
    
    except Exception as excepcion:
        sweetify.error(request, 'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect ('index')