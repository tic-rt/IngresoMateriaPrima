from django.urls import path

from shyma.views import guardar_rechazo, mostrar_en_transito, cargar_en_transito

urlpatterns = [
    path('en_transito/',mostrar_en_transito, name = 'en_transito'),
    path('ingreso/',cargar_en_transito, name='cargar_en_transito'),
    path('guardar_rechazo/',guardar_rechazo, name='guardar_rechazo')
]
