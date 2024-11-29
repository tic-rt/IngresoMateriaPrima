
from django.urls import path

from balanza.views import pendientes, pesaje


urlpatterns = [
    path('pendientes', pendientes,name='pendientesBalanza'),
    path('pesaje/', pesaje, name='pesaje'),
]