from django.shortcuts import redirect, render 
from django.contrib.auth.decorators import login_required
from personal.forms import FormPersonal
from personal.models import Personal
import sweetify

# Create your views here.

@login_required
def personal(request):
    """Esta funcion devuelve todos los responsables de sector"""

    responsables = Personal.objects.all()
    form_responsable = FormPersonal()

    return render(request,'personal/personal.html',
                {'responsables':responsables,
                'form_responsables':form_responsable})
    
@login_required
def agregarPersonal(request):
    """Esta funcion agrega un nuevo responsable a un area o sector"""
    try:
        if request.method == 'POST':
            formulario = FormPersonal(request.POST)
            
            if formulario.is_valid():
                formulario.save()
                sweetify.toast(request, 'Nuevo responsable agregado', icon="success", timer=5000)
                return redirect('personal')
            else:
                errores = []
                for campo, mensajes in formulario.errors.items():
                    for mensaje in mensajes:
                        errores.append(f'{campo}: {mensaje}')
                
                errores_str = '<br>'.join(errores)
                sweetify.warning(request,'Error al agregar empresa de transporte', text = errores_str, persistent = 'Aceptar')
                return redirect('personal')
            
    except Exception as excepcion:
        sweetify.error('Error al agregar Empresa de transporte', persistent=f'ocurrio un error {str(excepcion)}')
        return redirect('personal')

@login_required
def editarPersonal(request):
    """esta funcion edita un responsable"""
    try:
        if request.method == 'POST':
            id_responsable = request.POST.get('id')

            if Personal.objects.filter(id=id_responsable).exists():
                instancia = Personal.objects.get(id=id_responsable)
                form_editar = FormPersonal(instance=instancia)
                return render(request,'personal/editar.html',{'form_editar':form_editar})
            else:
                sweetify.error(request,'No permitido', text='EL agente no existe o fue eliminado')
                return redirect('personal')
    except Personal.DoesNotExist as excepcion:
        sweetify.error(request,'No permitido', text='EL agente no existe o fue eliminado')
        return redirect('personal')
    
    except Exception as excepcion:
        sweetify.error(request,'Error al editar', text=f'ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('personal')

@login_required
def eliminarPersonal(request):
    """Esta funcion elimina a un responsable a traves de su id"""
    try:
        if request.method == 'POST':
            id_responsable = request.POST.get('id')

            if Personal.objects.filter(id=id_responsable).exists():
                responsable = Personal.objects.get(id=id_responsable)
                responsable.delete()
                sweetify.success(request,'Agente eliminado', text=f'Se elimino a {responsable.__str__}')
                return redirect('personal')
            else:
                sweetify.error(request,'No permitido', text=('El agente fue eliminado o no existe'))
                return redirect('personal')
    except Personal.DoesNotExist as excepcion:
        sweetify.error(request,'No permitido', text='El agente fue eliminado o no existe')
        return redirect('personal')
    except Exception as excepcion:
        sweetify.error(request, 'Ocurrio un error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('personal')
    
@login_required
def actualizar(request):
    """Esta funcion actualiza Los datos de un agente"""
    try:
        if(request.method=='POST'):
            id_responsable = request.POST.get('id')
            instancia = Personal.objects.get(id=id_responsable)
            formulario = FormPersonal(request.POST, instance=instancia)

            if formulario.is_valid() and formulario :
                formulario.save()
                sweetify.success(request,'Agente actualizado', text='Los datos se han actualizado correctamente', timer=3000)
                return redirect('personal')
            else:
                errores = []

                for campo, mensajes in formulario.errors.items():
                    for mensaje in mensajes:
                        errores.append(f'{campo}: {mensaje}')
                        errores_str = '<br>'.join(errores)
                
                sweetify.warning(request,'Error al editar', text = errores_str, persistent = 'Aceptar')
                return redirect('personal')
            
    except Exception as excepcion:
        sweetify.error(request,'Ocurrio un error', text =f'Ocurrio un error {str(excepcion.__cause__)}', persistent='Aceptar')
        return redirect('personal')
