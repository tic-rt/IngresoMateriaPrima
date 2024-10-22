from django.urls import path
from personal.views import actualizar, agregarPersonal, editarPersonal, eliminarPersonal, personal


urlpatterns = [
    path('', personal, name='personal'),
    path('agregarPersonal/', agregarPersonal, name='agregarPersonal'),
    path('editarPersonal/', editarPersonal, name='editarPersonal'),
    path('eliminarpersonal',eliminarPersonal, name='eliminarPersonal'),
    path('actualizar', actualizar, name='actualizar')
]
