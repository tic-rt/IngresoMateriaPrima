from django.db import models

from base.models import Base
from hdr.models import HDR

# Create your models here.

class PamoPsul(Base):
    """Modelo para pamo y psul"""
    
    hora_ingreso = models.TimeField(verbose_name='Hora de Ingreso')
    presion = models.FloatField(verbose_name='Presion')
    temperatura = models.FloatField(verbose_name='Temperatura')
    hora_salida = models.TimeField(verbose_name='Hora de Salida')
    hdr = models.ForeignKey(HDR, on_delete=models.PROTECT, verbose_name='HDR')