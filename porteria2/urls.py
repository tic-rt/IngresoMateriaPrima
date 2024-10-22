
from django.urls import path

from porteria2.views import index, nuevoIngreso


urlpatterns = [
    path('',index,name='porteria2'),
    path('nuevoIngreso',nuevoIngreso,name='nuevoIngreso'),
]
