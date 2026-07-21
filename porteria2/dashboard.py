from django.utils import timezone
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from porteria2.models import Egreso, Ingreso


@login_required
@permission_required('porteria2.view_ingreso', login_url='index')
def index_porteria(request):
    """chart de vehiculos ingresados e informacion relevante para porteria"""
    return render(request, 'porteria2/porteria2.html')


def _obtener_fecha_inicio(periodo):
    """Devuelve la fecha de inicio segun el periodo solicitado"""
    hoy = timezone.now().date()
    if periodo == 'semana':
        return hoy - timezone.timedelta(days=6)
    elif periodo == 'mensual':
        return hoy.replace(day=1)
    return hoy  # 'hoy' por defecto


@login_required
@permission_required('porteria2.view_ingreso', login_url='index')
def dashboard_json(request):
    """JSON unificado del dashboard con filtro por periodo (?periodo=hoy|semana|mensual)"""
    periodo = request.GET.get('periodo', 'hoy')
    fecha_inicio = _obtener_fecha_inicio(periodo)
    hoy = timezone.now().date()

    # ---- Total ingresados por empresa (agrupado) ----
    ingresos = (
        Ingreso.objects
        .filter(hora_ingreso__date__gte=fecha_inicio, hora_ingreso__date__lte=hoy, is_deleted=False)
        .values('empresa_transporte__nombre')
        .annotate(cantidad=Count('id'))
        .order_by('-cantidad')
    )

    # ---- En transito por producto (agrupado) ----
    en_transito = (
        Ingreso.objects
        .filter(
            hora_ingreso__date__gte=fecha_inicio,
            hora_ingreso__date__lte=hoy,
            ingresado=True,
            hdr__estado='Activo',
            is_deleted=False
        )
        .values('producto__producto')
        .annotate(cantidad=Count('id'))
        .order_by('-cantidad')
    )

    # ---- Total general ingresados ----
    total_ingresados = (
        Ingreso.objects
        .filter(hora_ingreso__date__gte=fecha_inicio, hora_ingreso__date__lte=hoy, is_deleted=False)
        .count()
    )

    # ---- Total en transito ----
    total_transito = (
        Ingreso.objects
        .filter(
            hora_ingreso__date__gte=fecha_inicio,
            hora_ingreso__date__lte=hoy,
            ingresado=True,
            hdr__estado='Activo',
            is_deleted=False
        )
        .count()
    )

    # ---- Total rechazados ----
    total_rechazados = (
        Ingreso.objects
        .filter(
            hora_ingreso__date__gte=fecha_inicio,
            hora_ingreso__date__lte=hoy,
            hdr__estado='Rechazado',
            is_deleted=False
        )
        .count()
    )

    # ---- Total finalizados (egresos autorizados) ----
    total_finalizados = (
        Egreso.objects
        .filter(
            fecha_salida__date__gte=fecha_inicio,
            fecha_salida__date__lte=hoy,
            salida_autorizada=True,
            hdr__estado='Finalizado'
        )
        .count()
    )

    return JsonResponse({
        'ingresados_por_empresa': {
            'labels': [item['empresa_transporte__nombre'] for item in ingresos],
            'data': [item['cantidad'] for item in ingresos],
        },
        'en_transito_por_producto': {
            'labels': [item['producto__producto'] for item in en_transito],
            'data': [item['cantidad'] for item in en_transito],
        },
        'total_ingresados': total_ingresados,
        'total_transito': total_transito,
        'total_rechazados': total_rechazados,
        'total_finalizados': total_finalizados,
    })