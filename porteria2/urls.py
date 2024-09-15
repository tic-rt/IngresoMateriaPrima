
from django.urls import path

from porteria2.views import index


urlpatterns = [
    path('',index,name='porteria2')
]
