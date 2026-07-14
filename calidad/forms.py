from django import forms
from django.forms import ModelForm
from calidad.models import Calidad
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column,Div,HTML

class FormCalidad(ModelForm):
    class Meta:
        model = Calidad
        fields = '__all__'
        
        widgets = {
            'fecha_vigencia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'version': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'registro': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_registro(self):
        registro : str = self.cleaned_data.get('registro')

        if registro:
            registro = registro.upper()
            return registro
        
    def __init__(self, *args, **kwargs):
        super(FormCalidad, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Agregar nuevo registro'))
        self.helper.form_action = 'agregar_calidad'
        self.helper.layout = Layout(
            Div(
                Div(
                    HTML('<h3 class="text-center">Agregar nuevo registro</h3>'),
                    Row(
                        Column(Field('fecha_vigencia'), css_class='col-md-8'),
                    ),
                    Row(
                        Column(Field('version'), css_class='col-md-8'),
                    ),
                    Row(
                        Column(Field('registro'), css_class='col-md-8'),
                    ),
                    
                )
            )
        )
        