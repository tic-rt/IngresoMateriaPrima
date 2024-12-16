from django.urls import path
from pamo.views import pendientes


urlpatterns = [
    path('pendientes', pendientes, name='pendientesPAMO')
]