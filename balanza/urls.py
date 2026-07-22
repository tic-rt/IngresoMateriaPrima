
from django.urls import path

from balanza.views import balanza_index, guardarPesaje, guardarPesaje2, pendientes, pesaje, egresos, pesajeSalida
from balanza.dashboard import dashboard_kilos_json


urlpatterns = [
    path('inicio/', balanza_index, name='balanzaIndex'),
    path('pendientes', pendientes,name='pendientesBalanza'),
    path('pesaje/', pesaje, name='pesaje'),
    path('guardarPesaje/', guardarPesaje, name='guardarPesaje'),
    path('egresos',egresos, name='egresos'),
    path('pesajeSalida/', pesajeSalida, name='pesajeSalida'),
    path('guardarPesaje2/', guardarPesaje2, name='guardarPesaje2'),
    path('api/dashboard-kilos/', dashboard_kilos_json, name='dashboard_kilos'),
]
