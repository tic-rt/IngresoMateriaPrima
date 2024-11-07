from django.db import models

from base.models import Base

# Create your models here.

sector = [
   ('Porteria 2','Porteria 2'),
   ('Almacen PQ','Almacen PQ'),
   ('Inspeccion PQ','Inspeccion PQ'),
   ('PAMO/PSUL','PAMO/PSUL'),
]
estado=[
   ('Activo','Activo'),
   ('Anulado','Anulado'),
   ('Finalizado','Finalizado'),
   ('Rechazado','Rechazado')
]

class HDR(Base):
   fecha = models.DateTimeField(verbose_name='Feha', auto_now_add=True)
   sector = models.CharField(verbose_name= 'Sector', choices=sector, max_length=20, default='Porteria 2')
   estado=models.CharField(verbose_name='Estado', choices=estado, max_length=20, default='Activo')
   
   class Meta:
      """Meta defincion para HDR"""
      verbose_name = 'HDR'
      verbose_name_plural = 'HDR'



