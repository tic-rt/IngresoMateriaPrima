from django.urls import path
from psul.views import guardarPsul, pendientes, controlPsul


urlpatterns = [
    path('pendientes', pendientes, name='pendientesPSUL'),
    path('control/',controlPsul, name='controlPSUL'),
    path('guardarPSUL', guardarPsul, name='guardarPSUL')
]