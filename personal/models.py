from django.db import models

# Create your models here.

sectores = [
    ('Porteria 2', 'Porteria 2'),
    ('Inspeccion Quimica','Inspeccion Quimica'),
]

class Personal(models.Model):
    """Esta clase representa el personal responsable de cada áera"""
    
    sector = models.CharField(choices=sectores, max_length=100)
    nombre = models.CharField(verbose_name='Nombre',null=False, blank=False, max_length=30)
    apellido = models.CharField(verbose_name='Apellido', null=False, blank=False, max_length=30)
    legajo = models.CharField(verbose_name='Nº Legajo', null=False,blank=False, unique=True, max_length=5)
    is_deleted = models.BooleanField(verbose_name='Eliminado',default=False)
    
    class meta:
        """Meta definicion para Personal"""
        verbose_name = 'Personal'
        verbose_name = 'Personal'
        
    def __str__(self):
        return f'{self.nombre} {self.apellido} {self.legajo} '
    
    def delete(self, *args, **kwargs):#sof delete para mantener la integridad de la db
        self.is_deleted=True
        self.save()