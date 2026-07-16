from django.urls import path
from calidad.views import agregar_calidad, lista_calidad


urlpatterns = [
    path('gestion/', lista_calidad, name='gestion_calidad'),
    path('agregar/', agregar_calidad, name='agregar_calidad'),
]
