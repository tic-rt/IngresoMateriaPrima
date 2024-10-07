from django.urls import path
from transporte.views import (actualizar, agregarCamion, agregarConductor, agregarSemi, agregarTransporte, camiones, conductores, editarCamion, editarConductor, 
                              editarSemi, editarTransporte, eliminarCamion, eliminarConductor, eliminarSemi, eliminarTransporte, semis, transportes)  


urlpatterns = [
    path('', transportes, name='transportes'),
    path('camiones', camiones, name='camiones'),
    path('semis', semis, name='semis'),
    path('conductores', conductores, name='conductores'),
    path('agregarTransporte', agregarTransporte, name='agregarTransporte'),
    path('agregarCamion', agregarCamion, name='agregarCamion'),
    path('agregarSemi', agregarSemi, name='agregarSemi'),
    path('agregarConductor', agregarConductor, name='agregarConductor'),
    path('editarTransporte', editarTransporte, name='editarTransporte'),
    path('editarCamion', editarCamion, name='editarCamion'),
    path('editarSemi', editarSemi, name='editarSemi'),
    path('editarConductor', editarConductor, name = 'editarConductor'),
    path('eliminarTransporte', eliminarTransporte, name = 'eliminarTransporte'),
    path('eliminarCamion', eliminarCamion, name='eliminarCamion'),
    path('eliminarSemi', eliminarSemi, name ='eliminarSemi'),
    path('eliminarConductor', eliminarConductor, name='eliminarConductor'),
    path('actualizar/<str:modelo>',actualizar,name='actualizar'),
]
