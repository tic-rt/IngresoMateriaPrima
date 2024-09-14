from django.db import models

from base.models import Base

# Create your models here.

sectores = [
    ('Porteria 2', 'porteria 2'),
]

class Persona(models.Model):
    """Esta clase representa el personal responsable de cada áera"""
    
    sector = models.CharField(choices=sectores, max_length=100)
    nombre = models.CharField('Nombre', verbose_name='Nombre',null=False, blank=False, max_length=30)
    apellido = models.CharField('Apellido', verbose_name='Apellido', null=False, blank=False, max_length=30)
    legajo = models.CharField('Nº Legajo', verbose_name='Nº Legajo', null=False,blank=False, default=0, unique=True)
    
    class meta:
        """Meta definicion para Personal"""
        verbose_name = 'Personal'
        verbose_name = 'Personal'
        
    def __str__(self):
        return f'{self.nombre} {self.apellido} '
    