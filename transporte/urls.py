from django.urls import path

from transporte.views import transportes


urlpatterns = [
    path('',transportes,name='transportes')
]
