
from datetime import date
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Row,Column,Div,HTML
from django.urls import reverse
from personal.models import Personal
from porteria2.models import Ingreso
from transporte.models import Camion, Conductor, Semi, Transporte


class  FormIngreso(forms.ModelForm):
    """Formulario de ingreso de vehiculo a porteria 2"""

    class Meta:
        """Clase Meta para el formulario de ingreso"""
        
        model = Ingreso

        fields = [
            'ingreso_calefaccion',
            'empresa_transporte',
            'conductor',
            'producto',
            'patente_chasis',
            'patente_semi',
            'remito',
            'responsable'
        ]

        widgets={
            'ingreso_calefaccion':forms.CheckboxInput(attrs={
                'value':'True'}),
            'empresa_transporte':forms.Select(),
            'conductor':forms.Select(),
            'producto':forms.Select(),
            'remito':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Número de remito',
                'autocomplete':'off',
            }),
            'patente_chasis':forms.Select(),
            'patente_semi':forms.Select(),
            'responsable':forms.Select(attrs={
            'class':''
            }),
        }

    def __init__(self, *args, **kwargs):
        super(FormIngreso,self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit','Guardar'))
        self.fields['empresa_transporte'].queryset = Transporte.objects.filter(is_deleted = False)
        self.fields['empresa_transporte'].empty_label = 'Seleccione Empresa'
        hoy = date.today()
        self.fields['conductor'].queryset = Conductor.objects.none()
        self.fields['conductor'].empty_label='Seleccione un conductor'
        self.fields['patente_chasis'].queryset = Camion.objects.none()
        self.fields['patente_chasis'].empty_label = 'Seleccione un camión'
        self.fields['patente_semi'].queryset = Semi.objects.none()
        self.fields['patente_semi'].empty_label = 'Seleccione un semi'
        self.fields['responsable'].queryset = Personal.objects.filter( is_deleted = False)
        self.helper.form_action = reverse('guardarNuevoIngreso')
        self.helper.layout = Layout(
            Div(
                Div(
                    HTML('<h5 class="m-3">Empresa y Conductor</h5>'),
                    Row(
                        Column('empresa_transporte',css_class='col-6'),
                        Column('conductor',css_class='col-6'),
                    ),
                    css_class='border p-3 mb-3 shadow'
                ),
                Div(
                    HTML('<h5 class="m-3">Datos del vehículo</h5>'),
                    Row(
                    Column('patente_chasis',css_class='col-6'),
                    Column('patente_semi',css_class='col-6'),
                    ),
                    css_class='border p-3 mb-3 shadow'
                ),
                Div(
                    HTML('<h5> Datos del producto</h5>'),
                    Row(
                        Column('remito',css_class='col-7'),
                        Column('producto',css_class='col-5'),
                    ),
                    css_class='border p-3 mb-3 shadow'
                ),
                Div(
                    HTML('<h5>Calefación</h5>'),
                    Row(
                        Column('ingreso_calefaccion',css_class='col-4 col-sm-12')
                    ),
                    css_class='border p-3 mb-3 shadow'
                ),
                Div(
                    HTML('<h5> Responsable </h5>'),
                    Row(
                        Column('responsable',css_class='col-6'),
                    ),
                    css_class='border p-3 mb-3 shadow'
                )
            ),
        )