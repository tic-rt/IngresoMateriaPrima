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
        # Extraemos sector y sectores_disponibles como kwargs directos
        sector = kwargs.pop('sector', None)
        sectores_disponibles = kwargs.pop('sectores_disponibles', None)

        super().__init__(*args, **kwargs)

        if sectores_disponibles:
            if sector:
                self.fields['sector'].choices = [(sector, sectores_disponibles[sector])]
            else:
                self.fields['sector'].choices = list(sectores_disponibles.items())
        else:
            self.fields['sector'].choices = self.base_fields['sector'].choices

        # Si hay una instancia (edición), asegurar que su sector esté en las opciones
        if self.instance and self.instance.pk:
            instancia_sector = self.instance.sector
            if instancia_sector:
                sectores_actuales = dict(self.fields['sector'].choices)
                if instancia_sector not in sectores_actuales:
                    self.fields['sector'].choices = list(self.fields['sector'].choices) + [(instancia_sector, instancia_sector)]

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