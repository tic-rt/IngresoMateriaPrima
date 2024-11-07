from django.urls import path
from transporte.views import (actualizar, agregarCamion, agregarConductor, agregarSemi, agregarTransporte, camiones, conductores, editarCamion, editarConductor, 
                              editarSemi, editarTransporte, eliminarCamion, eliminarConductor, eliminarSemi, eliminarTransporte, obtenerCamiones, obtenerConductores, obtenerSemis, semis, transportes)  


urlpatterns = [
    path('', transportes, name='transportes'),
    path('camiones', camiones, name='camiones'),
    path('semis', semis, name='semis'),
    path('conductores', conductores, name='conductores'),
    path('agregarTransporte', agregarTransporte, name='agregarTransporte'),
    path('editarTransporte', editarTransporte, name='editarTransporte'), 
    path('eliminarTransporte', eliminarTransporte, name = 'eliminarTransporte'),
    path('agregarCamion', agregarCamion, name='agregarCamion'),
    path('editarCamion', editarCamion, name='editarCamion'),
    path('eliminarCamion', eliminarCamion, name='eliminarCamion'),
    path('obtenerCamiones', obtenerCamiones, name='obtenerCamiones'),
    path('agregarSemi', agregarSemi, name='agregarSemi'),
    path('editarSemi', editarSemi, name='editarSemi'),
    path('eliminarSemi', eliminarSemi, name ='eliminarSemi'),
    path('obtenerSemis',obtenerSemis,name='obtenerSemis'),
    path('agregarConductor', agregarConductor, name='agregarConductor'),
    path('editarConductor', editarConductor, name = 'editarConductor'),
    path('eliminarConductor', eliminarConductor, name='eliminarConductor'),
    path('obtenerConductores',obtenerConductores,name='obtenerConductores'),
    path('actualizar/<str:modelo>',actualizar,name='actualizar'),
]
