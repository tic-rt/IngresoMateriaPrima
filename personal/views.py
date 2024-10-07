from django.shortcuts import render

from personal.forms import FormPersonal
from personal.models import Personal

# Create your views here.

def personal(request):
    """Esta funcion devuelve todos los responsables de sector"""

    responsables = Personal.objects.all()
    form_responsable = FormPersonal()

    return render(request,'personal/personal.html',
                  {'responsables':responsables,
                   'form_responsables':form_responsable})
