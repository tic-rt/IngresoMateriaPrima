
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
            'responsable_entrada',
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
            'responsable_entrada':forms.Select(attrs={'class':'form-control'}),
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
        self.fields['responsable_entrada'].queryset = Personal.objects.filter(is_deleted = False, sector = 'Almacen PQ')
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
                    Column('responsable_entrada',css_class='col-6'),
                    css_class='mb-3'),
                )
            )
        
class FormBalanzaSalida(forms.ModelForm):
    """Formulario para el peso de un vehiculo a la salida"""

    class Meta:
        """Clase Meta para el formulario de balanza"""

        model = Balanza

        fields = [
            'fecha_salida',
            'peso_fmrt',
            'peso_vacio',
            'peso_taquilla',
            'peso_bolsa_tarima',
            'peso_neto',
            'responsable_salida',
            ]

        widgets = {
            'fecha_salida':forms.DateTimeInput(attrs={'class':'form-control entrada',
                                                  'readonly':'readonly'},),
            'peso_fmrt':forms.NumberInput(attrs={
                'class':'form-control entrada',
                'min':0,
                'data-bs-toggle':'tooltip',
                'data-bs-title':'Peso expresado en kilogramos',
                'data-bs-placement':'bottom'
                }),
            'peso_vacio':forms.NumberInput(attrs={
                'class':'form-control entrada',
                'data-bs-toggle':'tooltip',
                'data-bs-title':'Peso expresado en kilogramos',
                'data-bs-placement':'bottom',
                'min':0}),
            'peso_taquilla':forms.NumberInput(attrs={
                'class':'form-control',
                'data-bs-toggle':'tooltip',
                'data-bs-title':'Peso expresado en kilogramos',
                'data-bs-placement':'bottom',
                'value':0,
                'min':0}),
            'peso_bolsa_tarima':forms.NumberInput(attrs={
                'class':'form-control',
                'data-bs-toggle':'tooltip',
                'data-bs-title':'Peso expresado en kilogramos',
                'data-bs-placement':'bottom',
                'min':0}),
            'peso_neto': forms.NumberInput(attrs={
                'class':'form-control peso_neto',
                'data-bs-toggle':'tooltip',
                'data-bs-title':'Peso Expresado en Kilogramos',
                'data-bs-placement':'bottom',
                'min':0,
                'readonly':'readonly'
                }),
            'responsable_salida':forms.Select(attrs={
                'class':'form-control',
                }),
            }
        
    def __init__(self, *args, **kwargs):
        super(FormBalanzaSalida, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('Submit', 'Guardar pesaje'))
        self.fields['responsable_salida'].queryset = Personal.objects.filter(is_deleted = False, sector = 'Almacen PQ')
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('fecha_salida',css_class='col-3')),
                Row(
                    Column('proveedor',css_class='col-4'),
                    Column('remito',css_class='col-4'),
                    Column('peso_origen',css_class='col-4'),
                    css_class='mb-3'),
                Row(
                    Column('observaciones')
                    ),
                Row(
                    Column('responsable_salida',css_class='col-6'),
                    css_class='mb-3'),
                )
            )