
from django import forms
from django.forms import ModelForm

from transporte.models import Camion, Semi, Transporte


class FormTransporte(ModelForm):
    """Formulario basado en modelo Transporte"""
    
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
    """Formulario basado en Camion"""

    class Meta:
        
        model = Camion

        fields = [
            'transporte',
            'marca',
            'patente',
            'vencimiento_seguro'
        ]

        widgets = {
            'transporte':forms.Select(attrs={'class':'form-control'}),
            'marca': forms.Select(attrs={'class':'form-control'}),
            'patente':forms.TextInput(attrs={'type':'text','class':'form-control','placeholder':'Patente del camión','autocomplete':'off'}),
            'vencimiento_seguro':forms.DateInput(attrs={'type':'date','class':'form-control'}),
        }
        
    def clean_patente(self):
        patente : str = self.cleaned_data.get('patente')

        if patente :
            patente = patente.upper()
            return patente

class FormSemi(ModelForm):
    """formulario basado en Semi"""

    class Meta:
        model = Semi

        fields = [
            'transporte',
            'patente',
            'vencimiento_seguro'
        ]
        
        widgets={
            'transporte':forms.Select(attrs={'class':'form-control'}),
            'patente': forms.TextInput(attrs={'class':'form-control','placeholder':'Patente del semi','autocomplete':'off'}),
            'vencimiento_seguro' :forms.DateInput(attrs={'type':'date','class':'form-control'})
        }
        
    def clean_patente(self):
        patente : str = self.cleaned_data.get('patente')
        
        if patente:
            patente = patente.upper()
            return patente        