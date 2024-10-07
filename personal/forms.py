from django import forms
from django.forms import ModelForm

from personal.models import Personal


class FormPersonal(ModelForm):

    class Meta:
        model = Personal

        fields = [
            'nombre',
            'apellido',
            'legajo'
        ]

        widgets = { #hermosear con helper de crispy y usar tag
            'nombre': forms.TextInput(attrs={
                'type':'text',
                'class':'form-control',
                'placeholder':'Nombre',
                'autocomplete':'off',
                }),
            'apellido': forms.TextInput(attrs={
                'type':'text',
                'class':'form-control',
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