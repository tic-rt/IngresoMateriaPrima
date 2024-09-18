from django.urls import path

from transporte.views import agregarTransporte, transportes


urlpatterns = [
    path('',transportes,name='transportes'),
    path('agregarTransporte',agregarTransporte, name='agregarTransporte')
]
