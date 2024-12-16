from django.db import models

from base.models import Base

# Create your models here.
""" productos = [ # No deberia estar hardcodeado ,por ahora puede salir asi,esta es la lista completa?  
    ('Azufre','Azufre Líquido'),
    ('Azufre sólido','Azufre sólido o a granel'),
    ('Amoníaco','Amoníaco'),
] """

class Producto(Base):
    """Productos que se van a recibir """
    nombre = models.TextField(max_length=100, verbose_name='Producto',blank=False, null=False, default='')
    
    class Meta:
        """Meta para definicion de Producto"""

        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Proveedor(Base):
    """Los proveedores que entregaran Producto"""
    nombre = models.TextField(verbose_name='Proveedor',max_length=50)
    
    class Meta:
        """Meta para la definicion de Proveedores"""
        
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class ProveedorProducto(Base):
    """ modelo Proveedor has Producto """
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, verbose_name='Proveedor')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name='Producto')

    class Meta:
        """Meta pata la definicion de provvedorProducto"""

        verbose_name = 'Proveedor Producto'
        verbose_name_plural = 'Proveedores Productos'

    def __str__(self):
        return f'{self.proveedor.nombre} {self.producto}'
    
    