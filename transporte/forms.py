
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
            'nombre': forms.TextInput(attrs={
                'type':'text',
                'class':'form-control cap',
                'placeholder':'Nombre de empresa de transporte',
                'autocomplete':'off'})
        }
        
    def clean_nombre(self):
        nombre : str = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.title()
            return nombre
        
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
            'vencimiento_seguro':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'patente':forms.TextInput(attrs={'type':'text','class':'form-control','placeholder':'Patente del camión'})
        }
        
    def clean_patente(self):
        patente : str = self.cleaned_data.get('patente')
        if patente :
            patente = patente.upper()
            return patente
       