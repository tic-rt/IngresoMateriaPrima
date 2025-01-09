# Create your models here.

from django.db import models
from base.models import Base
from hdr.models import HDR
from personal.models import Personal
from porteria2.models import Ingreso
from proveedores.models import Proveedor


class Balanza(Base):
    hora_ingreso = models.DateTimeField(verbose_name='Hora de Ingreso')
    proveedor =models.ForeignKey(Proveedor, on_delete=models.PROTECT, verbose_name='Proveedor')
    remito =  models.CharField(verbose_name='Remito',blank=False, null=False, max_length=100, default='')
    peso_origen = models.IntegerField(verbose_name='Peso de Origen',blank=False,null=False,default=0)
    #destino = models.TextField(max_length=100,default='Fabrica Militar Rio Tercero', blank=False, null=False )
    responsable_entrada = models.ForeignKey(Personal,on_delete=models.PROTECT, verbose_name='Responsable Entrada', related_name='responsable_entrada')
    observaciones = models.TextField(max_length=100,default='DOD según el IN 11-IQ-07', blank=False, null=False)
    hdr = models.ForeignKey(HDR, on_delete=models.PROTECT, verbose_name='HDR')
    fecha_salida = models.DateTimeField(verbose_name='Fecha de Salida', null=True)
    peso_fmrt = models.IntegerField(verbose_name='Peso en FMRT',blank=False, null=True, default=0)
    peso_vacio = models.IntegerField(verbose_name='Peso vacio',blank=False, null=True, default=0)
    peso_taquilla = models.IntegerField(verbose_name='Peso taquilla',blank=False, null=False, default=0)
    peso_bolsa_tarima = models.IntegerField(verbose_name='Peso bolsa/tarima', blank=False, null=False, default=0)
    peso_neto = models.IntegerField(verbose_name='Peso neto', blank=False,null=True, default=0)
    responsable_salida = models.ForeignKey(Personal,on_delete=models.PROTECT,verbose_name='Responsable Salida',related_name='responsable_salida', null=True)
    class Meta:
        """Meta definicion para el modelo Balanza"""
        verbose_name = 'Balanza'
        verbose_name_plural = 'Balanza'

""" class Destino(models.Model):
    destino = models.TextField(verbose_name='Destino',max_length='200',blank=False, null=False,default='') """
