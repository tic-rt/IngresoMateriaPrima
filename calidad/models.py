from django.db import models

class Calidad(models.Model):
    """Esta clase representa los datos da calidad de la HDR"""

    fecha_vigencia = models.DateTimeField(verbose_name='Fecha de Vigencia')
    version = models.IntegerField(verbose_name='Versión', null=False, blank=False)
    registro = models.CharField(verbose_name='Registro', max_length=100, null=False, blank=False)

    def __str__(self):
        return f'{self.version} - {self.fecha_vigencia} - {self.registro}'
