from django.urls import path
from pamo.views import guardarPamo, pendientes, controlPamo


urlpatterns = [
    path('pendientes', pendientes, name='pendientesPAMO'),
    path('control/',controlPamo, name='controlPAMO'),
    path('guardarPAMO', guardarPamo, name='guardarPAMO')
]