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