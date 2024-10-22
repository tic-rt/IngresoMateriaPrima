from django.db import models
from base.models import Base
from personal.models import Personal
from proveedores.models import Producto
from transporte.models import Camion, Semi, Transporte, Conductor

# Create your models here.

class Ingreso(Base):
    """Esta clase representa el Ingreso de un vehiculo para descarga en la porteria es 1 de n etapas de la HDR"""

    horaIngreso = models.DateTimeField(verbose_name="Hora de Ingreso",auto_now_add=True)
    ingresoCalefaccion = models.BooleanField(verbose_name='Ingreso para calefaccion de cisterna')
    empresaTransporte = models.ForeignKey(Transporte,on_delete=models.PROTECT)
    conductor = models.ForeignKey(Conductor,on_delete=models.PROTECT) 
    producto = models.ForeignKey(Producto,on_delete=models.PROTECT)
    remito = models.CharField(verbose_name='Remito',blank=False, null=False, max_length=100)
    patenteChasis = models.ForeignKey(Camion,on_delete=models.PROTECT)
    patenteSemi  = models.ForeignKey(Semi, on_delete=models.PROTECT)
    responsable = models.ForeignKey(Personal, on_delete=models.PROTECT)
    ingresado = models.BooleanField(verbose_name='Ingresado',null=False, default=False)
    
    class Meta:
        """Meta definicion para la clase Ingreso"""
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'