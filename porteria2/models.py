from django.db import models
from base.models import Base
from hdr.models import HDR
from personal.models import Personal
from proveedores.models import Producto
from transporte.models import Camion, Semi, Transporte, Conductor

# Create your models here.

class Ingreso(Base):
    """Esta clase representa el Ingreso de un vehiculo para descarga en la porteria es 1 de n etapas de la HDR,ingresado =False hasta que supera control de epp"""

    hora_ingreso = models.DateTimeField(verbose_name="Hora de Ingreso", auto_now_add=True)
    ingreso_calefaccion = models.BooleanField(verbose_name='Ingreso para calefaccion de cisterna')
    empresa_transporte = models.ForeignKey(Transporte, on_delete=models.PROTECT)
    conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    remito = models.CharField(verbose_name='Remito',blank=False, null=False, max_length=100,unique=True)
    patente_chasis = models.ForeignKey(Camion, on_delete=models.PROTECT)
    patente_semi = models.ForeignKey(Semi, on_delete=models.PROTECT)
    responsable = models.ForeignKey(Personal, on_delete=models.PROTECT)
    ingresado = models.BooleanField(verbose_name='Ingresado', null=False, default=False)
    laborable = models.BooleanField(verbose_name='Dia Laborable', null = False, default = True)
    hdr = models.ForeignKey(HDR, on_delete=models.PROTECT)

    class Meta:
        """Meta definicion para la clase Ingreso"""
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'

class Egreso(Base):
    """Esta clase registra la salida de los vehiculos una vez completado el circuito"""
    fecha_salida = models.DateTimeField(verbose_name='Fecha de Salida',auto_now_add=True)
    verificacion = models.BooleanField(verbose_name='verificacion de vehiculo/carga', default=False)
    salida_autorizada = models.BooleanField(verbose_name='Salida Autorizada', default=False)
    responsable = models.ForeignKey(Personal,on_delete=models.PROTECT)
    hdr = models.ForeignKey(HDR,on_delete=models.PROTECT)

class EPP(models.Model):
    """Esta clase registra los elementos de proteccion personal de un conductor"""
    fecha_control = models.DateTimeField(verbose_name='Fecha de Control', auto_now_add=True)
    casco = models.BooleanField(verbose_name='casco', default=False)
    mascara = models.BooleanField(verbose_name='mascara', default=False)
    antiparras = models.BooleanField(verbose_name='antiparras PVC', default=False)
    botines = models.BooleanField(verbose_name='botines', default=False)
    pantalon_camisa = models.BooleanField(verbose_name='pantalon/camisa/mameluco anti-ácido', default=False)
    matafuego = models.BooleanField(verbose_name='matafuego', default=False)
    arrestallamas = models.BooleanField(verbose_name='arrestallamas')
    carteleria = models.BooleanField(verbose_name='carteleria', default=False)
    responsable = models.ForeignKey(Personal, on_delete=models.PROTECT)
    hdr = models.ForeignKey(HDR, on_delete=models.PROTECT)

    class Meta:
        """Meta definicion para la clase EPP"""
        verbose_name = 'EPP'
        verbose_name_plural = 'EPP'
        