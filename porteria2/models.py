from django.db import models
from base.models import Base
from hdr.models import HDR
from personal.models import Personal
from proveedores.models import Producto
from transporte.models import Camion, Semi, Transporte, Conductor

# Create your models here.

class Ingreso(Base):
    """Esta clase representa el Ingreso de un vehiculo para descarga en la porteria es 1 de n etapas de la HDR"""

    hora_ingreso = models.DateTimeField(verbose_name="Hora de Ingreso",auto_now_add=True)
    ingreso_calefaccion = models.BooleanField(verbose_name='Ingreso para calefaccion de cisterna')
    empresa_transporte = models.ForeignKey(Transporte,on_delete=models.PROTECT)
    conductor = models.ForeignKey(Conductor,on_delete=models.PROTECT) 
    producto = models.ForeignKey(Producto,on_delete=models.PROTECT)
    remito = models.CharField(verbose_name='Remito',blank=False, null=False, max_length=100)
    patente_chasis = models.ForeignKey(Camion,on_delete=models.PROTECT)
    patente_semi  = models.ForeignKey(Semi, on_delete=models.PROTECT)
    responsable = models.ForeignKey(Personal, on_delete=models.PROTECT)
    ingresado = models.BooleanField(verbose_name='Ingresado',null=False, default=False)
    hdr = models.ForeignKey(HDR, on_delete=models.PROTECT)
    
    class Meta:
        """Meta definicion para la clase Ingreso"""
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'