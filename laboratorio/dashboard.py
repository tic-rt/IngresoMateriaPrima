from django.utils import timezone
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from laboratorio.models import Inspeccion


def _obtener_fecha_inicio(periodo):
    """Devuelve la fecha de inicio segun el periodo solicitado"""
    hoy = timezone.now().date()
    if periodo == 'semana':
        return hoy - timezone.timedelta(days=6)
    elif periodo == 'mensual':
        return hoy.replace(day=1)
    elif periodo == 'anual':
        return hoy.replace(month=1, day=1)
    return hoy  # 'hoy' por defecto


@login_required
@permission_required('porteria2.view_ingreso', login_url='index')
def index_laboratorio(request):
    """dashboard con gráficos de laboratorio"""
    return render(request, 'laboratorio/index_laboratorio.html')


@login_required
@permission_required('porteria2.view_ingreso', login_url='index')
def dashboard_inspecciones_json(request):
    """JSON: inspecciones aceptadas/rechazadas agrupadas por producto o proveedor.
    ?filtro=producto|proveedor&periodo=hoy|semana|mensual|anual"""
    filtro = request.GET.get('filtro', 'producto')
    periodo = request.GET.get('periodo', 'hoy')
    fecha_inicio = _obtener_fecha_inicio(periodo)
    hoy = timezone.now().date()

    # Si filtro es 'proveedor', agrupar por empresa_transporte
    if filtro == 'proveedor':
        group_field = 'hdr__ingreso__empresa_transporte__nombre'
    else:
        group_field = 'hdr__ingreso__producto__producto'

    datos = (
        Inspeccion.objects
        .filter(fecha__date__gte=fecha_inicio, fecha__date__lte=hoy)
        .values(group_field)
        .annotate(
            aceptados=Count('id', filter=Q(certificado=True, requisitos=True)),
            rechazados=Count('id', filter=~Q(certificado=True, requisitos=True))
        )
        .order_by('-aceptados')
    )

    labels = [item[group_field] for item in datos]
    aceptados = [item['aceptados'] for item in datos]
    rechazados = [item['rechazados'] for item in datos]

    return JsonResponse({
        'labels': labels,
        'aceptados': aceptados,
        'rechazados': rechazados,
        'total_aceptados': sum(aceptados),
        'total_rechazados': sum(rechazados),
    })