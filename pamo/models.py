from django.db import models

from base.models import Base
from hdr.models import HDR
from personal.models import Personal

# Create your models here.

class PamoPsul(Base):
    """Modelo para pamo y psul"""
        
    hora_ingreso = models.TimeField(verbose_name='Hora de Ingreso')
    presion_ingreso = models.FloatField(verbose_name='Presión Ingreso', null=True)
    temperatura_ingreso = models.FloatField(verbose_name='Temperatura Ingreso', null=True)
    presion_salida = models.FloatField(verbose_name='Presión Salida', null=True)
    temperatura_salida = models.FloatField(verbose_name='Temperatura Salida', null=True)
    hora_salida = models.TimeField(verbose_name='Hora de Salida')
    responsable = models.ForeignKey(Personal, on_delete=models.PROTECT,verbose_name='Responsable')
    hdr = models.ForeignKey(HDR, on_delete=models.PROTECT, verbose_name='HDR')