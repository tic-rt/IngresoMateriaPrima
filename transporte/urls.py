from django.urls import path
from transporte.views import (actualizar, agregarCamion, agregarConductor, agregarSemi, agregarTransporte, camiones, conductores, editarCamion, 
                              editarSemi, editarTransporte, eliminarCamion, eliminarSemi, eliminarTransporte, semis, transportes)  


urlpatterns = [
    path('', transportes, name='transportes'),
    path('camiones', camiones, name='camiones'),
    path('semis', semis, name='semis'),
    path('conductores', conductores, name='conductores'),
    path('agregarTransporte', agregarTransporte, name='agregarTransporte'),
    path('agregarCamion', agregarCamion, name='agregarCamion'),
    path('agregarSemi', agregarSemi, name='agregarSemi'),
    path('agregarConductor', agregarConductor, name='agregarConductor'),
    path('eliminarTransporte', eliminarTransporte, name = 'eliminarTransporte'),
    path('editarTransporte', editarTransporte, name='editarTransporte'),
    path('eliminarCamion', eliminarCamion, name='eliminarCamion'),
    path('eliminarSemi', eliminarSemi, name ='eliminarSemi'),
    path('editarCamion', editarCamion, name='editarCamion'),
    path('eliminarCamion', eliminarCamion, name='eliminarCamion'),
    path('editarSemi', editarSemi, name='editarSemi'),
    path('actualizar/<str:modelo>',actualizar,name='actualizar'),
]
