from django.shortcuts import redirect, render
import sweetify

from balanza.forms import FormBalanza
from porteria2.models import Ingreso

# Create your views here.

def pendientes(request):
    """Funcion que devuelve todos los ingresos autorizados y que siguen a balanza"""

    try:
        ingresos = Ingreso.objects.filter(is_deleted = False, ingresado = True )
        return render(request,'balanza/pendientes.html',{'ingresos':ingresos})
    except Exception as excepcion:
        sweetify.error(request,'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('index')

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