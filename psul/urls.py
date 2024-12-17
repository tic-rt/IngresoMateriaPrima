from django.urls import path
from psul.views import pendientes


urlpatterns = [
    path('pendientes', pendientes, name='pendientesPSUL')
]