
from django import forms

from porteria2.models import Ingreso


class  formIngreso(forms.Model):
    class Meta:
        model = Ingreso
        fields = [
            'ingresoCalefaccion',
            'empresaTransporte',
            'conductor',
            'producto',
            'patenteChasis',
            'patenteSemi',
            'responsable'
        ]