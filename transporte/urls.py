from django.urls import path

from transporte.views import agregarCamion, agregarSemi, agregarTransporte, camiones, semis, transportes


urlpatterns = [
    path('',transportes,name='transportes'),
    path('camiones',camiones,name='camiones'),
    path('semis',semis,name='semis'),
    path('agregarTransporte',agregarTransporte, name='agregarTransporte'),
    path('agregarCamion',agregarCamion,name='agregarCamion'),
    path('agregarSemi',agregarSemi,name='agregarSemi')
]
