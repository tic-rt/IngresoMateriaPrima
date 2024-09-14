from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
# Create your models here.

class Base(models.Model):
    """Base para los modelos que necesiten un id y registro de cambios"""
    
    id=models.AutoField(primary_key=True)
    created_date = models.DateField('Fecha de creación', auto_now=False, auto_now_add=True)
    modified_date = models.DateField('Fecha de Modificacion', auto_now=True, auto_now_add=False)
    deleted_date = models.DateField('Fecha de eliminacion')
    historical = HistoricalRecords(user_model=User, inherit=True)
    
    property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        """Meta defincion para Base ."""
        abstract = True
        verbose_name = 'Modelo Base'
        verbose_name_plural = 'Modelos Base'