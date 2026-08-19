from django.db import models

from base.models import Base
from personal.models import Personal

# Create your models here.

sector = [
   ('Porteria 2','Porteria 2'),
   ('Porteria 2 E','Porteria 2 E'),
   ('Almacen PQ','Almacen PQ'),
   ('Almacen PQ E','Almacen PQ E'),
   ('Inspeccion PQ','Inspeccion PQ'),
   ('PAMO','PAMO'),
   ('PSUL','PSUL')
]
estado=[
   ('Activo','Activo'),
   ('Anulado','Anulado'),
   ('Finalizado','Finalizado'),
   ('RechazoConfirmado','RechazoConfirmado'),
   ('Rechazado','Rechazado')
]

class HDR(Base):
   fecha = models.DateTimeField(verbose_name='Feha', auto_now_add=True)
   sector = models.CharField(verbose_name= 'Sector', choices=sector, max_length=20, default='Porteria 2')
   estado=models.CharField(verbose_name='Estado', choices=estado, max_length=20, default='Activo')
   observacion = models.CharField(verbose_name='Observaciones', max_length=200,blank=True, default='')
   rechazado_por = models.ForeignKey(Personal, verbose_name='Rechazado por', on_delete=models.PROTECT, null=True, blank=True)
   
   class Meta:
      """Meta defincion para HDR"""
      verbose_name = 'HDR'
      verbose_name_plural = 'HDR'



