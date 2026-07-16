from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from calidad.forms import FormCalidad   
from calidad.models import Calidad

@login_required
@permission_required('calidad.view_calidad', login_url='login')
def lista_calidad(request):
    """Funcion que devuelve lista de datos de calidad y el formulario para agregar nuevos datos"""
    calidad = Calidad.objects.all().order_by('-fecha_vigencia')[:5]
    form_calidad = FormCalidad()
    return render(request,'calidad/gestion.html', {'calidad': calidad, 'form_calidad': form_calidad})

def agregar_calidad(request):
    """Funcion que agrega un nuevo registro de calidad a la base de datos"""
    if request.method == 'POST':
        form = FormCalidad(request.POST)
        if form.is_valid():
            form.save()
    return redirect('gestion_calidad')