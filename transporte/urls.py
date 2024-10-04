from django.urls import path

from transporte.views import actualizar, agregarCamion, agregarSemi, agregarTransporte, camiones, editarCamion, editarTransporte, eliminarCamion, eliminarTransporte, semis, transportes  


urlpatterns = [
    path('', transportes, name='transportes'),
    path('camiones', camiones, name='camiones'),
    path('semis', semis, name='semis'),
    path('agregarTransporte', agregarTransporte, name='agregarTransporte'),
    path('agregarCamion', agregarCamion, name='agregarCamion'),
    path('agregarSemi', agregarSemi, name='agregarSemi'),
    path('eliminarTransporte', eliminarTransporte, name = 'eliminarTransporte'),
    path('editarTransporte', editarTransporte, name='editarTransporte'),
    path('editarCamion', editarCamion, name='editarCamion'),
    path('eliminarCamion', eliminarCamion, name='eliminarCamion'),
    path('actualizar/<str:modelo>',actualizar,name='actualizar')

]
