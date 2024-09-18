
from django import forms
from django.forms import ModelForm

from transporte.models import Camion, Transporte


class FormTransporte(ModelForm):
    
    class Meta:
        
        model = Transporte
        fields = [
            'nombre'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'type':'text','class':'form-control cap'})
        }
        
class FormCamion(ModelForm):

    class Meta:
        
        model = Camion
        fields = [
            'transporte',
            'marca',
            'patente',
            'vencimiento_seguro'
        ]
        widgets = {
            'vencimiento_seguro':forms.DateInput(attrs={'type':'date','class':'form-control'})
        }
       