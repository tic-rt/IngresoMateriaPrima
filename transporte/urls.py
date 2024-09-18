from django.urls import path

from transporte.views import agregarCamion, agregarTransporte, transportes


urlpatterns = [
    path('',transportes,name='transportes'),
    path('agregarTransporte',agregarTransporte, name='agregarTransporte'),
    path('agregarCamion',agregarCamion,name='agregarCamion'),
]
