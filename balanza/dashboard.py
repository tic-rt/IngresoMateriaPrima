from django.utils import timezone
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required

from balanza.models import Balanza


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
def dashboard_kilos_json(request):
    """JSON: Kilos totales agrupados por producto o proveedor segun filtro (?filtro=producto|proveedor&periodo=hoy|semana|mensual)"""
    filtro = request.GET.get('filtro', 'producto')
    periodo = request.GET.get('periodo', 'hoy')
    fecha_inicio = _obtener_fecha_inicio(periodo)
    hoy = timezone.now().date()

    queryset = Balanza.objects.filter(
        hora_ingreso__date__gte=fecha_inicio,
        hora_ingreso__date__lte=hoy,
        is_deleted=False
    )

    if filtro == 'proveedor':
        # Agrupar por proveedor
        datos = (
            queryset
            .values('proveedor__nombre')
            .annotate(total_kilos=Sum('peso_neto'), cantidad=Count('id'))
            .order_by('-total_kilos')
        )
        labels = [item['proveedor__nombre'] for item in datos]
        data = [item['total_kilos'] for item in datos]
    else:
        # Agrupar por producto (default)
        datos = (
            queryset
            .values('hdr__ingreso__producto__producto')
            .annotate(total_kilos=Sum('peso_neto'), cantidad=Count('id'))
            .order_by('-total_kilos')
        )
        labels = [item['hdr__ingreso__producto__producto'] for item in datos]
        data = [item['total_kilos'] for item in datos]

    total_kilos = sum(data)

    return JsonResponse({
        'labels': labels,
        'data': data,
        'total_kilos': total_kilos,
    })