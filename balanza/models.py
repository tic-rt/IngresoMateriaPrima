# Create your models here.

from django.db import models
from base.models import Base
from hdr.models import HDR
from personal.models import Personal
from porteria2.models import Ingreso
from proveedores.models import Proveedor


class Balanza(Base):
    hora_ingreso = models.DateField(verbose_name='Hora de Ingreso')
    proveedor =models.ForeignKey(Proveedor, on_delete=models.PROTECT, verbose_name='Proveedor')
    remito = models.ForeignKey(Ingreso,on_delete=models.PROTECT, verbose_name='Remito Nº')
    peso_origen = models.IntegerField(verbose_name='Peso de Origen',blank=False,null=False,default=0)
    #destino = models.TextField(max_length=100,default='Fabrica Militar Rio Tercero', blank=False, null=False )
    responsable = models.ForeignKey(Personal,on_delete=models.PROTECT, verbose_name='Responsable')
    observaciones = models.TextField(max_length=100,default='DOD según el IN 11-IQ-07', blank=False, null=False)
    hdr = models.ForeignKey(HDR, on_delete=models.PROTECT, verbose_name='HDR')

    class Meta:
        """Meta definicion para el modelo Balanza"""
        verbose_name = 'Balanza'
        verbose_name_plural = 'Balanza'

""" class Destino(models.Model):
    destino = models.TextField(verbose_name='Destino',max_length='200',blank=False, null=False,default='') """
