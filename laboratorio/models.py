from django.db import models

from base.models import Base
from hdr.models import HDR
from personal.models import Personal

# Create your models here.

class Inspeccion(Base):
    """clase que define el modelo de inspeccion quimica"""
    fecha = models.DateTimeField(verbose_name='Fecha de Inspeccion', auto_now_add=True)
    certificado = models.BooleanField(verbose_name='Ingresa con certificado')
    requisitos = models.BooleanField(verbose_name='Cumple requisitos')
    descargar = models.BooleanField(verbose_name='Autorizado a descargar',default=True)
    responsable = models.ForeignKey(Personal, on_delete=models.PROTECT)
    observacion = models.TextField(verbose_name='observacion', max_length=200, blank=True, null=True)
    cerrado = models.BooleanField(verbose_name='Cerrado', default=False)
    hdr = models.OneToOneField(HDR, on_delete=models.PROTECT, verbose_name='HDR')