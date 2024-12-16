from django import forms
import pamoPsul


class formPamoPsul(forms.modelForm):
    """formulario para PamoPsul"""

    class Meta:
        model = pamoPsul

        fields = [
            'hora_ingreso',
            'presion',
            'temperatura',
            'hora_salida']

        widgets = {
            'hora_ingreso': forms.TimeInput(attrs=
                                            {'class':'form-control',
                                             'required':'true'}),
            'presion': forms.NumberInput(attrs={'required':'true',
                                                'class':'form-control',
                                                'min':0,
                                                'step':0.1,
                                                'placeholder':'ingrese la presión'}),
            'temperatura': forms.NumberInput(attrs={'required':'true',
                                                    'class':'form-control',
                                                    'min':0,
                                                    'step':0.1,
                                                    'placeHolder':'Ingrese la temperatura'}),
            'hora_salida': forms.TimeInput(attrs={'required':'true',
                                                  'class' : 'form-control'})
            }

        