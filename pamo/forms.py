from django import forms

from pamo.models import PamoPsul
from personal.models import Personal


class formPamo(forms.ModelForm):
    
    responsable = forms.ModelChoiceField(queryset=Personal.objects.filter(is_deleted=False, sector='PAMO'),
                                             widget=forms.Select(attrs={'class':'form-control'}),
                                             empty_label='Seleccione un responsable')
     
    class Meta:
        model = PamoPsul
        fields = ('hora_ingreso',
                  'presion_ingreso',
                  'temperatura_ingreso',
                  'presion_salida',
                  'temperatura_salida',
                  'responsable',
                  'hora_salida')
        
        widgets ={
            'hora_ingreso':forms.TimeInput(attrs={'class':'form-control',
                                           'required':'true',
                                           'type':'time'}),
            'presion_ingreso': forms.NumberInput(attrs={'class':'form-control',
                                                'required':'true',
                                                'min':0,
                                                'step':0.1}),
            'temperatura_ingreso':forms.NumberInput(attrs={'class':'form-control',
                                                   'required':'true',
                                                   'min':0,
                                                   'step':0.1}),
             'presion_salida': forms.NumberInput(attrs={'class':'form-control',
                                                'required':'true',
                                                'min':0,
                                                'step':0.1}),
            'temperatura_salida':forms.NumberInput(attrs={'class':'form-control',
                                                   'required':'true',
                                                   'min':0,
                                                   'step':0.1}),
            'hora_salida':forms.TimeInput(attrs={'class':'form-control',
                                                 'required':'true',
                                                 'type':'time'}),
            }
        
        
        