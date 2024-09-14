from django.db import models

from base.models import Base

# Create your models here.

class Transporte(Base):
    nombre = models.CharField('transporte',verbose_name='Transporte', max_length=50)