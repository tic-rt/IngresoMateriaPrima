from django.db import models

from base.models import Base
from hdr.models import HDR
from personal.models import Personal

# Create your models here.

class Inspeccion(Base):
    """clase que define el modelo de inspeccion quimica"""

    hora_extraccion = models.DateTimeField(verbose_name='Hora Extracción')
    certificado = models.BooleanField(verbose_name='Ingresa con certificado')
    requisitos = models.BooleanField(verbose_name='Cumple requisitos')
    responsable = models.ForeignKey(Personal, on_delete=models.PROTECT)
    observacion = models.TextField(verbose_name='observacion', max_length=200, blank=True, null=True)
    hdr = models.ForeignKey(HDR, on_delete=models.PROTECT, verbose_name='HDR')