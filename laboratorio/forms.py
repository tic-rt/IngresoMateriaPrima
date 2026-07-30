
from django import forms
from crispy_forms.helper import FormHelper,Layout
from crispy_forms.layout import Row, Column, Submit

from laboratorio.models import Inspeccion
from personal.models import Personal


class FormLaboratorio(forms.ModelForm):
    """formulario para inspeccion quimica"""
    CERTIFICADO_CHOICES = [
        (None, 'Seleccione una opción'),  # Opción vacía para "Seleccione una opción"
        (True, 'Sí'),
        (False, 'No'),
    ]
    
    REQUISITOS_CHOICES = [
        (None, 'Seleccione una opción'),
        (True, 'Sí'),
        (False, 'No'),
    ]

    DESCARGA_CHOICES = [
            (None, 'Seleccione una opción'),
            (True, 'Sí'),
            (False, 'No'),
        ]
    
    certificado = forms.ChoiceField(choices=CERTIFICADO_CHOICES, required=True)
    requisitos = forms.ChoiceField(choices=REQUISITOS_CHOICES, required=True)
    descargar = forms.ChoiceField( choices=DESCARGA_CHOICES, required=True)

    class Meta:
        model = Inspeccion
        
        fields = [
        'certificado',
        'requisitos',
        'descargar',
        'responsable',
        'observacion']

        widgets = {
            'certificado':forms.Select(attrs={'class':'form-control'}),
            'requisitos':forms.Select(attrs={'class':'form-control'}),
            'descargar':forms.Select(attrs={'class':'form-control'}),
            'responsable':forms.Select(attrs={'class':'form-control'}),
            'observacion':forms.Textarea(attrs=
                                           {'class':'form-control',
                                            'placeholder':'Observaciones',
                                            'rows':3})}

    def __init__(self, *args, **kwargs):
        super(FormLaboratorio, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['responsable'].queryset = Personal.objects.filter(is_deleted = False, sector = 'Inspeccion Quimica')
        self.fields['certificado'].empty_label = 'Seleccione una opción'
        self.fields['requisitos'].empty_label = 'Seleccione una opción'
        self.fields['descargar'].empty_label = 'Seleccione una opcion'
        self.helper.add_input(Submit('Submit','Guardar'))
        self.helper.layout = Layout(
            Row(
                Column('certificado', css_class='col-4'),
                Column('requisitos', css_class='col-4'),
                Column('descargar',css_class='col-4'),
                css_class='mb-3',
                ),
            Row(
                Column('observacion'),
                css_class='mb-3',
                ),
            Row(
                Column('responsable', css_class='col-6'),
                css_class='d-flex justify-content-center')
            )