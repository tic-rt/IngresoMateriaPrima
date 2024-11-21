from django.db import models

from base.models import Base

# Create your models here.
productos = [ # No deberia estar hardcodeado ,por ahora puede salir asi,esta es la lista completa?  
    ('Azufre','Azufre Liquido'),
    ('Azufre solido','Azufre solido a granel'),
    ('Amoniaco','Amoniaco'),
]

class Producto(Base):
    """Productos que se van a recibir """
    producto = models.CharField(choices=productos,max_length=100)
    
    class Meta:
        """Meta para definicion de Producto"""

        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['producto']
    
    def __str__(self):
        return self.producto
    
        
            
class Proveedores(Base):
    """Los proveedores que entregaran Producto"""
    nombre = models.CharField(verbose_name='Proveedor',max_length=50)
    producto = models.ForeignKey(Producto,on_delete=models.PROTECT,verbose_name='Producto', null=False)
    
    class Meta:
        """Meta para la definicion de Proveedores"""
        
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
    