from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from porteria2.models import Egreso, Ingreso

# Create your views here.

@login_required
def index(request):
    return render(request,'app/index.html')

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
    hoy = timezone.now()
    ingresos_en_curso = Ingreso.objects.filter(ingresado = True, hdr__estado='Activo').count()
    en_transito = Ingreso.objects.filter(ingresado = True, hdr__estado='Activo').count()
    ingresos_finalizados = Egreso.objects.filter(salida_autorizada = True, hdr_id__estado='Finalizado',fecha_salida = hoy).count()
    
    return JsonResponse({
        'labels': ['Ingreso','En transito', 'Finalizados'],
        'data': [ingresos_en_curso, en_transito, ingresos_finalizados],
    })