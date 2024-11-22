
from django.urls import path

from porteria2.views import controlEpp, guardarControlEpp, guardarNuevoIngreso, guardarRechazo, index, mostrarControlEpp, nuevoIngreso


urlpatterns = [
    path('', index, name='porteria2'),
    path('nuevoIngreso', nuevoIngreso, name='nuevoIngreso'),
    path('guardarNuevoIngreso', guardarNuevoIngreso, name='guardarNuevoIngreso'),
    path('controlEpp/', controlEpp, name='controlEpp'),
    path('controlEppPendientes', mostrarControlEpp, name='controlEppPendientes'),
    path('guardarControlEpp/', guardarControlEpp, name='guardarControlEpp'),
    path('guardarRechazo/', guardarRechazo, name='guardarRechazo')
]
