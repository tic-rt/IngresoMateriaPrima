from django import forms
from django.forms import ModelForm

from personal.models import Personal


class FormPersonal(ModelForm):

    class Meta:
        model = Personal

        fields = [
            'sector',
            'nombre',
            'apellido',
            'legajo'
        ]

        widgets = { #hermosear con helper de crispy y usar tag
            'sector' : forms.Select(attrs={
                'class':'form-control',
            }),
            'nombre': forms.TextInput(attrs={
                'type':'text',
                'class':'form-control text-capitalize',
                'placeholder':'Nombre',
                'autocomplete':'off',
                }),
            'apellido': forms.TextInput(attrs={
                'type':'text',
                'class':'form-control text-capitalize',
                'placeholder':'Apellido',
                'autocomplete':'off'
            }),
            'legajo': forms.TextInput(attrs={
                'type':'text',
                'class':'form-control',
                'pattern' : '[0-9]*',
                'placeholder':'Número de Legajo',
                'autocomplete':'off'
            })
        }

    def __init__(self, *args, **kwargs):
        # Extraemos el sector y los sectores disponibles de 'initial'
        sector = kwargs.get('initial', {}).get('sector', None)
        sectores_disponibles = kwargs.get('initial', {}).get('sectores_disponibles', {})

        super().__init__(*args, **kwargs)

        # Establecemos las opciones del campo 'sector' en función de los sectores disponibles
        if sector:
            # Si el sector está definido (especificado por la vista), solo mostramos ese sector
            self.fields['sector'].choices = [(sector, sectores_disponibles[sector])]
        else:
            # Si no se define un sector específico, mostramos todos los sectores disponibles
            self.fields['sector'].choices = list(sectores_disponibles.items())

        # Si ya hay un sector inicial, lo asignamos
        if sector:
            self.fields['sector'].initial = sector
            
    def clean_nombre(self):
        nombre :str = self.cleaned_data.get('nombre')

        if nombre :
            nombre = nombre.capitalize()
            return nombre
    
    def clean_apellido(self):
        apellido :str = self.cleaned_data.get('apellido')

        if apellido :
            apellido = apellido.capitalize()
            return apellido