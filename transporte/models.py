from django.db import models

from base.models import Base

# Create your models here.

class Transporte(Base):
    """Esta clase representa una empresa de transporte"""
    
    nombre = models.CharField(verbose_name='Transporte', max_length=50, unique=True)
    
    class Meta:
        """Metas definicion para Transporte"""
        
        verbose_name = 'Empresa de Transporte'
        verbose_name_plural = 'Empresas de Transporte'
        
    def __str__(self):
            return self.nombre
        
class Camion(Base):
    """Esta clase representa un camion que pertenece a una empresa de transporte"""
    
    marcas = [
            ('Mercedes-Benz', 'Mercedes-Benz'),
            ('Volvo', 'Volvo'),
            ('Scania', 'Scania'),
            ('Iveco', 'Iveco'),
            ('Ford', 'Ford'),
            ('MAN', 'MAN'),
            ('Hino', 'Hino'),
            ('Isuzu', 'Isuzu'),
            ('Chevrolet', 'Chevrolet'),
            ('Kenworth', 'Kenworth'),
            ]
    
    transporte = models.ForeignKey(Transporte, on_delete=models.PROTECT, verbose_name='Transporte')
    marca = models.CharField(verbose_name='Marca',choices=marcas,max_length=30)
    patente = models.CharField(verbose_name='Patente', max_length=10, null=False, blank=False, default='AAA000AAA')
    vencimiento_seguro = models.DateField(verbose_name='Vencimiento Seguro') #Preguntar si va o no va
    
    class Meta:
        """Meta definicion  para Camion"""
        
        verbose_name = 'Camión'
        verbose_name_plural = 'Camiones'
    
    def __str__(self):
        return f'{self.marca} {self.patente}'
     
             
class Semi(Base):
    """Esta clase representa un semi que pertenece a una empresa de transporte"""
    
    transporte = models.ForeignKey(Transporte, on_delete=models.PROTECT, verbose_name='Transporte')
    patente = models.CharField(verbose_name='Patente', max_length=10, null=False, blank= False, default='AAA000AAA')
    vencimientoSeguro = models.DateField(verbose_name='Vencimiento Seguro Semi') #Preguntar si va o no va 
    
    class Meta:
        """Meta definicion para el Semi de una empresa de transporte"""
        
        verbose_name = 'Semi'
        verbose_name_plural = 'Semis'
    
    def __str__(self):
        return f'Semi {self.patente}'
    
class Conductor(Base):
    transporte = models.ForeignKey(Transporte,on_delete=models.PROTECT,verbose_name='Transporte')
    nombre = models.CharField(verbose_name='Nombre', null=False, blank=False, max_length=30)
    apellido = models.CharField(verbose_name='Apellido', null=False, blank= False, max_length=30)
    dni = models.CharField(verbose_name='DNI',blank=False, null= False, unique=True,  max_length=15)
    vencimientoCarnet = models.DateField(verbose_name='Vencimiento Carnet', blank=False, null=False)
    #Que mas del conductor??hablar con ramos
    #Finalizar esto!!!
    
    class Meta:
        """Meta definicion para el conductor  de una empresa de transporte"""
    
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'