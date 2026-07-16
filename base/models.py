from django.utils import timezone
from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
# Create your models here.

class Base(models.Model):
    """Base para los modelos que necesiten un id y registro de cambios"""
    
    id=models.AutoField(primary_key=True)
    created_date = models.DateField('Fecha de creación', auto_now_add=True)
    modified_date = models.DateField('Fecha de Modificacion', auto_now=True)
    deleted_date = models.DateField('Fecha de eliminacion',blank=True, null=True)
    is_deleted = models.BooleanField('Eliminado',default=False)
    historical = HistoricalRecords(user_model=User, inherit=True)
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    #Soft delete (para choferes camiones etc, mantenerlos para mantener la integridad verificar Si funciona, creo que no)   
    def delete(self, *args, **kwargs):
        self.deleted_date = timezone.now() 
        self.is_deleted = True
        self.save()  

    
    def restore(self):
        self.deleted_date = None
        self.is_deleted = False
        self.save()


    class Meta:
        """Meta defincion para Base ."""
        abstract = True