
from django.urls import path
from hdr.views import exportar_hdr, lista_hdr


urlpatterns = [
    path("lista/", lista_hdr, name="lista_hdr"),
    path("exportar/", exportar_hdr, name="exportar_hdr"),
]
