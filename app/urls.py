from django.urls import path

from app.views import cantidad_camiones, index,transito


urlpatterns = [
    path('',index,name='index'),
    path('cantidad_camiones/',cantidad_camiones,name='cantidad_camiones'),
    path('transito/',transito,name='transito'),
]
