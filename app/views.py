from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from porteria2.dashboard import index_porteria, dashboard_json
from balanza.dashboard import dashboard_kilos_json
from laboratorio.dashboard import dashboard_inspecciones_json

from porteria2.models import Egreso, Ingreso

# Create your views here.

@login_required
def index(request):
    ingresos = Ingreso.objects.filter(ingresado = True, hdr__estado='Activo')
    cantidad = ingresos.count()
    return render(request,'app/index.html',{
                                            'ingresos':ingresos, 
                                            'cantidad':cantidad
                                            })

def cantidad_camiones(request):
    hoy = timezone.now()
    cant_amoniaco = Ingreso.objects.filter(producto__producto ='Amoníaco',created_date = hoy,ingresado = True).count()
    cant_azufre_liquido = Ingreso.objects.filter(producto__producto='Azufre Líquido',created_date = hoy,ingresado = True).count()
    cant_azufre_solido = Ingreso.objects.filter(producto__producto='Azufre solido o a granel',created_date = hoy,ingresado = True).count()
    cant_hipoclorito = Ingreso.objects.filter(producto__producto='Hipoclorito',created_date = hoy,ingresado = True).count()
    datos = {
        'Amoniaco': cant_amoniaco,
        'Azufre Liquido': cant_azufre_liquido,
        'Azufre solido o a granel': cant_azufre_solido,
        'Hipoclorito': cant_hipoclorito,
        }
    return JsonResponse({
                         'labels': list(datos.keys()),
                         'data': list(datos.values()),
                         })
    
def transito(request):
    hoy = timezone.now().date()
    print(hoy)
    ingresos_en_curso = Ingreso.objects.filter(ingresado = True,hora_ingreso__date=hoy).count()
    en_transito = Ingreso.objects.filter(ingresado = True,hora_ingreso__date=hoy, hdr__estado='Activo').count()
    ingresos_finalizados = Egreso.objects.filter(salida_autorizada = True, hdr__estado='Finalizado',fecha_salida__date = hoy).count()
    
    data = {
        'labels': ['Ingreso','En transito', 'Finalizados'],
        'data': [ingresos_en_curso, en_transito, ingresos_finalizados],
    }
    print("DEBUG BACKEND:", data)
    
    return JsonResponse({
        'labels': ['Ingreso','En transito', 'Finalizados'],
        'data': [ingresos_en_curso, en_transito, ingresos_finalizados],
    })