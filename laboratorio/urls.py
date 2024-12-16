
from django.urls import path

from laboratorio.views import inspeccion, pendientes


urlpatterns = [
    path('pendientes',pendientes,name='pendientesInspeccion'),
    path('inspeccion/', inspeccion, name='inspeccion'),
]