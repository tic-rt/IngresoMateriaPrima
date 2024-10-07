from django.urls import path
from personal.views import personal


urlpatterns = [
    path('', personal, name='personal'),
]
