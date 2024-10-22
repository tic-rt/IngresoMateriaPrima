
from django import forms

from porteria2.models import Ingreso


class  formIngreso(forms.Model):
    """Formulario de ingreso de vehiculo a porteria 2"""

    class Meta:
        """Clase Meta para el formulario de ingreso"""
        
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