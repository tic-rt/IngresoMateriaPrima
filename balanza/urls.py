
from django.urls import path

from balanza.views import guardarPesaje, pendientes, pesaje


urlpatterns = [
    path('pendientes', pendientes,name='pendientesBalanza'),
    path('pesaje/', pesaje, name='pesaje'),
    path('guardarPesaje/', guardarPesaje, name='guardarPesaje')
]