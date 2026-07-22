
from django.urls import path

from laboratorio.views import guardarInspeccion, inspeccion, pendientes
from laboratorio.dashboard import index_laboratorio, dashboard_inspecciones_json


urlpatterns = [
    path('',index_laboratorio,name='index_laboratorio'),
    path('pendientes',pendientes,name='pendientesInspeccion'),
    path('inspeccion/', inspeccion, name='inspeccion'),
    path('guardarinspeccion/', guardarInspeccion, name='guardarInspeccion'),
    path('api/dashboard-inspecciones/', dashboard_inspecciones_json, name='dashboard_inspecciones'),
]
