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
   ('Activo','Activo')
   ('Finalizado','Finalizado'),
   ('Rechazado','Rechazado')
]

class HDR(Base):
   fecha = models.DateTimeField(verbose_name='Feha')
   sector = models.CharField(verbose_name= 'Sector',choices=sector, max_length=20)
   estado=models.CharField(verbose_name='Estado',choices=estado, max_length=20)
   
   class Meta:
      """Meta defincion para HDR"""
      verbose_name = 'HDR'
      verbose_name_plural = 'HDR'



