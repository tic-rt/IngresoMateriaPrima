
from django.urls import path

from laboratorio.views import guardar_inspeccion, inspeccion, pendientes, pendientes_control,guardar_inspeccion_pendiente,inspeccion_pendiente
from laboratorio.dashboard import index_laboratorio, dashboard_inspecciones_json


urlpatterns = [
    path('',index_laboratorio,name='index_laboratorio'),
    path('pendientes',pendientes,name='pendientesInspeccion'),
    path('inspeccion/', inspeccion, name='inspeccion'),
    path('guardar_inspeccion/', guardar_inspeccion, name='guardarInspeccion'),
    path('inspeccion_pendiente/', pendientes_control, name = 'inspeccion_pendiente' ),
    path('control_inspeccion/',inspeccion_pendiente, name = 'control_inspeccion_pendiente'),
    path('guardar_inspeccion_pendiente',guardar_inspeccion_pendiente,name = 'guardar_inspeccion_pendiente'),
    path('api/dashboard-inspecciones/', dashboard_inspecciones_json, name='dashboard_inspecciones'),
]
