from django.db import models

# Create your models here.

sectores = [
    ('Porteria 2', 'porteria 2'),
]

class Personal(models.Model):
    """Esta clase representa el personal responsable de cada áera"""
    
    sector = models.CharField(choices=sectores, max_length=100)
    nombre = models.CharField(verbose_name='Nombre',null=False, blank=False, max_length=30)
    apellido = models.CharField(verbose_name='Apellido', null=False, blank=False, max_length=30)
    legajo = models.CharField(verbose_name='Nº Legajo', null=False,blank=False, default=0, unique=True)
    
    class meta:
        """Meta definicion para Personal"""
        verbose_name = 'Personal'
        verbose_name = 'Personal'
        
    def __str__(self):
        return f'{self.nombre} {self.apellido} '
    