from django import forms

from hdr.models import HDR


class FormHDR(forms.ModelForm):
    class Meta:
        model = HDR
        fields =['observacion']

        widgets={'observacion': forms.Textarea(attrs={'class':'form-control',
                                                  'row':10,
                                                  'cols':50,
                                                  'placeholder':'Observacion',
                                                  'maxlength':200,
                                                  'autofocus':'autofocus'})}