from django.db import models

from base.models import Base

# Create your models here.
class Producto(Base):
    """Productos que se van a recibir """
    nombre = models.TextField('Producto',verbose_name='Producto')
    
    class Meta:
        """Meta para definicion de Producto"""

        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']
        
            
class Proveedores(Base):
    """Los proveedores que entregaran Producto"""
    nombre = models.TextField('Proveedor', verbose_name='Proveedor')
    producto = models.ForeignKey(Producto,on_delete=models.PROTECT,verbose_name='Producto', null=False)
    
    class Meta:
        """Meta para la definicion de Proveedores"""
        
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']
    
    