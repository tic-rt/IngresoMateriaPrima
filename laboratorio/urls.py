
from django.urls import path

from laboratorio.views import guardarInspeccion, inspeccion, pendientes


urlpatterns = [
    path('pendientes',pendientes,name='pendientesInspeccion'),
    path('inspeccion/', inspeccion, name='inspeccion'),
    path('guardarinspeccion/', guardarInspeccion, name='guardarInspeccion')
]