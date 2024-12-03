
from django import forms

from balanza.models import Balanza
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Div,Row,Column

from personal.models import Personal


class FormBalanza(forms.ModelForm):
    """Formulario para el peso de un vehiculo"""

    class Meta:
        """Clase Meta para el formulario de balanza"""

        model = Balanza

        fields = [
            'proveedor',
            'remito',
            'peso_origen',
            'responsable',
            'observaciones'
            ]

        widgets = {
            'proveedor':forms.Select(attrs={'class':'form-control'}),
            'remito':forms.TextInput(attrs={
                'class':'form-control',
                'data-bs-toggle':'tooltip',
                'data-bs-title':'Si se detecta inconsistencia se debera verificar con Porteria 2',
                'data-bs-placement':'bottom'}),
            'peso_origen': forms.NumberInput(attrs={
                'class':'form-control',
                'data-bs-toggle':'tooltip',
                'data-bs-title':'Peso Expresado en Kilogramos',
                'data-bs-placement':'bottom',
                'min':"0",
                }),
            'responsable':forms.Select(attrs={'class':'form-control'}),
            'observaciones':forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'DOD según el IN 11-IQ-07',
                'rows':3,
                }),
            }
    def __init__(self, *args, **kwargs):
        super(FormBalanza, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('Submit', 'Guardar pesaje'))
        self.fields['responsable'].queryset = Personal.objects.filter(is_deleted = False, sector = 'Almacen PQ')
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('proveedor',css_class='col-4'),
                    Column('remito',css_class='col-4'),
                    Column('peso_origen',css_class='col-4'),
                    css_class='mb-3'),
                Row(
                    Column('observaciones')
                    ),
                Row(
                    Column('responsable',css_class='col-6'),
                    css_class='mb-3'),
                )
            )
        