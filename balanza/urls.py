
from django.urls import path

from balanza.views import guardarPesaje, guardarPesaje2, pendientes, pesaje, egresos, pesajeSalida


urlpatterns = [
    path('pendientes', pendientes,name='pendientesBalanza'),
    path('pesaje/', pesaje, name='pesaje'),
    path('guardarPesaje/', guardarPesaje, name='guardarPesaje'),
    path('egresos',egresos, name='egresos'),
    path('pesajeSalida/', pesajeSalida, name='pesajeSalida'),
    path('guardarPesaje2/', guardarPesaje2, name='guardarPesaje2')
    
]