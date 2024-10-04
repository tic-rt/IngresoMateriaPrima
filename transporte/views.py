from django.utils import timezone
from django.shortcuts import redirect, render

from transporte.forms import FormCamion, FormSemi, FormTransporte
from transporte.models import Camion, Conductor, Semi, Transporte
import sweetify

# Create your views here.

def transportes(request):
    """Esta funcion devolvera todas las empresas de transportes registradas junto a los formularios correspondientes para la carga"""
    
    transportes = Transporte.objects.filter(is_deleted = False)
    form_transporte = FormTransporte()

    return render(request,'transporte/transportes.html', 
                  {'transportes':transportes,
                   'form_transporte': form_transporte
                   })

def camiones(request):
    """Esta funcion devolvera todos los camiones de transportes registrados junto a los formularios correspondientes para la carga"""
    
    camiones = Camion.objects.filter(is_deleted = False)
    hoy = timezone.now().date()
    form_camion = FormCamion()

    return render(request,'transporte/camiones.html', 
                  {'camiones':camiones,
                   'form_camion':form_camion,
                   'hoy':hoy
                   })

def semis(request):
    """Esta funcion devolvera todos los semis de transportes registradas junto a los formularios correspondientes para la carga"""
    
    semis = Semi.objects.filter(is_deleted = False)
    hoy = timezone.now().date()
    form_semi = FormSemi()

    return render(request,'transporte/semis.html', 
                  {'semis':semis,
                   'form_semi': form_semi,
                   'hoy':hoy
                   })

def choferes(request):
    """Esta funcion devolvera todos los conductores registrados, junto a los formularios correspondientes para la carga"""
    choferes = Conductor.objects.filter(is_deleted = False)
    pass

def agregarTransporte(request):
    """esta funcion agrega una empresa de transporte nueva"""

    try:
        if request.method == 'POST':
            transporte = FormTransporte(request.POST)
            
            if(transporte.is_valid()):
                 #transporte.save()
                 sweetify.toast(request,f'Empresa de transporte {transporte.clean_nombre()} agregada',icon='success',timer = 5000)
                 return redirect('transportes')
            
            else:
                errores = []
                for campo, mensajes in transporte.errors.items():
                    for mensaje in mensajes:
                        errores.append(f'{campo}: {mensaje}')
                
                errores_str = '<br>'.join(errores)
                sweetify.warning(request,'Error al agregar empresa de transporte', text = errores_str, persistent = 'Aceptar')
                return redirect('transportes')
            
    except Exception as excepcion :
        sweetify.error('Error al agregar Empresa de transporte', persistent=f'ocurrio un error {str(excepcion)}')
        return redirect('transportes')
    
def agregarCamion(request):
    """Esta funcion agrega un nuevo camion"""

    try:
        if request.method == 'POST':
            camion = FormCamion(request.POST)

            if(camion.is_valid()):
                camion.save()
                sweetify.toast(request,f'Camion patente {camion.clean_patente()} agregado', icon='success', timer=5000)
                return redirect('camiones')
            
            else:
                errores = []
                for campo, mensajes in camion.errors.items():
                    for mensaje in mensajes:
                        errores.append(f'{campo}: {mensaje}')  

                errores_str = '<br>'.join(errores)
                sweetify.warning(request,'Error al agregar empresa de transporte', text = errores_str, persistent = 'Aceptar')
                return redirect('camiones')
            
    except Exception as excepcion:
        sweetify.error(request,'Error al agregar camion',persistent=f'ocurrio un error {str(excepcion)}')
        return redirect('camiones')
            
def agregarSemi(request):
    """Esta funcion agrega un nuevo semi"""

    try:
        if request.method == 'POST':
            semi = FormSemi(request.POST)

            if semi.is_valid():
                semi.save()
                sweetify.toast(request,f'Semi patente {semi.clean_patente()} agregado',icon='success', timer=5000)
                return redirect('semis')
            
            else:
                errores = []
                for campo, mensajes in semi.errors.items():
                    for mensaje in mensajes:
                        errores.append(f'{campo}: {mensaje}')  

                    errores_str = '<br>'.join(errores)
                    sweetify.warning(request,'Error al agregar empresa de transporte', text = errores_str, persistent = 'Aceptar')
                    return redirect('semis')
                
    except Exception as excepcion:
        sweetify.error(request,'Error al agregar camion',persistent=f'ocurrio un error {str(excepcion)}')
        return redirect('semis')
    
def editarTransporte(request):#porque no la haces generica?que venga que tipo es y lo filtras/editar/int/tipo
    """Esta funcion edita una empresa por su id"""
    
    try:
        if request.method == 'POST':
            id_empresa = request.POST.get('id')
           
            if Transporte.objects.filter(id=id_empresa, is_deleted=False).exists():
                transporte = Transporte.objects.filter(id=id_empresa).get()
                form_editar = FormTransporte(instance=transporte)
                modelo = 'Transporte'
                return render(request,'transporte/editar.html',{'form_editar':form_editar,'modelo':modelo})
            
            else:
                sweetify.warning(request, 'No permitido', text='La empresa no existe o ya fue eliminada')
                return redirect('transportes')
            
    except Transporte.DoesNotExist as excepcion:#lo estoy considerando en el else, ver
            sweetify.warning(request, 'No permitido', text='La empresa no existe o ya fue eliminada')
            return redirect('transportes')
    
    except Exception as excepcion:
        sweetify.error(request, 'Error al editar', text=f'Ocurrió un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('transportes')

def editarCamion(request):#porque no la haces generica?que venga que tipo es y lo filtras/editar/int/tipo
    """Esta funcion edita un camion por su id"""
    
    try:
        if request.method == 'POST':
            id_camion = request.POST.get('id')
            if Camion.objects.filter(id=id_camion, is_deleted=False).exists():
                camion = Camion.objects.filter(id=id_camion).get()
                form_editar = FormCamion(instance=camion)
                modelo = 'Camion'
                return render(request,'transporte/editar.html',{'form_editar':form_editar,'modelo':modelo})
            
            else:
                sweetify.warning(request, 'No permitido', text='El camion no existe o ya fue eliminada')
                return redirect('camiones')
            
    except Transporte.DoesNotExist as excepcion:#lo estoy considerando en el else, ver
            sweetify.warning(request, 'No permitido', text='El camion no existe o ya fue eliminada')
            return redirect('camiones')
    
    except Exception as excepcion:
        sweetify.error(request, 'Error al editar', text=f'Ocurrió un error {str(excepcion)}', persistent = 'Aceptar')
        print(id_camion)
        return redirect('camiones')

def editarSemi(request):#porque no la haces generica?que venga que tipo es y lo filtras/editar/int/tipo
    """Esta funcion edita un semi por su id"""
    
    try:
        if request.method == 'POST':
            id_semi = request.POST.get('id')
            if Semi.objects.filter(id=id_semi, is_deleted=False).exists():
                semi = Semi.objects.filter(id=id_semi).get()
                form_editar = FormSemi(instance=semi)
                modelo = 'Semi'
                return render(request,'transporte/editar.html',{'form_editar':form_editar,'modelo':modelo})
            
            else:
                sweetify.warning(request, 'No permitido', text='El semi no existe o ya fue eliminada')
                return redirect('semis')
            
    except Transporte.DoesNotExist as excepcion:#lo estoy considerando en el else, ver
            sweetify.warning(request, 'No permitido', text='El semi no existe o ya fue eliminada')
            return redirect('semis')
    
    except Exception as excepcion:
        sweetify.error(request, 'Error al editar', text=f'Ocurrió un error {str(excepcion)}', persistent = 'Aceptar')
        print(id_semi)
        return redirect('semis')

def eliminarTransporte(request):
    """Esta funcion elimina una empresa de transporte por su id   print('entrando a eliminar')"""

    try:
        if request.method == 'POST':
            
            id_empresa = request.POST.get('id')

            if Transporte.objects.filter(id=id_empresa, is_deleted=False).exists():  # si no existe lanza la excepcion

                transporte = Transporte.objects.get(id=id_empresa)
                #transporte.delete()  # Eliminar el transporte
                sweetify.success(request, 'Empresa Eliminada', text=f'La empresa {transporte.nombre} ha sido eliminada', timer = 3000)
                return redirect('transportes')
            else:
                sweetify.warning(request, 'No permitido', text='La empresa no existe o ya fue eliminada')
                return redirect('transportes')
            
    except Transporte.DoesNotExist as excepcion:
        sweetify.error(request, 'Error al eliminar', text='La empresa que intentas eliminar no existe o no se encuentra', persistent='aceptar')
        return redirect('transportes')
    
    except Exception as excepcion:
        sweetify.error(request, 'Error al eliminar', text=f'Ocurrió un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('transportes')
    
def eliminarCamion(request):
    """Esta funcion elimina un camion de transporte por su id """

    try:
        if request.method == 'POST':
            
            id_camion = request.POST.get('id')

            if Camion.objects.filter(id=id_camion, is_deleted=False).exists():  # si no existe lanza la excepcion

                camion = Camion.objects.get(id=id_camion)
                #transporte.delete()  # Eliminar el transporte
                sweetify.success(request, 'Camion Eliminado', text=f'El camion {camion.patente} de la empresa {camion.transporte.nombre}  ha sido eliminado', timer = 3000)
                return redirect('camiones')
            else:
                sweetify.warning(request, 'No permitido', text='El camion no existe o ya fue eliminado')
                return redirect('camiones')
            
    except Transporte.DoesNotExist as excepcion:
        sweetify.error(request, 'Error al eliminar', text='El camion que intentas eliminar no existe o no se encuentra', persistent='aceptar')
        return redirect('camiones')
    
    except Exception as excepcion:
        sweetify.error(request, 'Error al eliminar', text=f'Ocurrió un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('camiones')
    
def eliminarSemi(request):
    """Esta funcion elimina un camion de transporte por su id """

    try:
        if request.method == 'POST':
            
            id_semi = request.POST.get('id')

            if Semi.objects.filter(id=id_semi, is_deleted=False).exists():  # si no existe lanza la excepcion

                semi = Semi.objects.get(id=id_semi)
                #transporte.delete()  # Eliminar el transporte
                sweetify.success(request, 'Semi Eliminado', text=f'El Semi {semi.patente} de la empresa {semi.transporte.nombre}  ha sido eliminado', timer = 3000)
                return redirect('semis')
            else:
                sweetify.warning(request, 'No permitido', text='El semi no existe o ya fue eliminado')
                return redirect('semis')
            
    except Transporte.DoesNotExist as excepcion:
        sweetify.error(request, 'Error al eliminar', text='El semi que intentas eliminar no existe o no se encuentra', persistent='aceptar')
        return redirect('semis')
    
    except Exception as excepcion:
        sweetify.error(request, 'Error al eliminar', text=f'Ocurrió un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('camiones')
    
def actualizar(request,modelo):
    """La funcion recibe un formulario, identifica el tipo y lo actualiza"""
    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            formulario = None
            instancia = None

            match modelo:

                case 'Transporte':
                    instancia = Transporte.objects.get(id=id)
                    formulario = FormTransporte(request.POST, instance=instancia)

                case 'Camion':
                    instancia = Camion.objects.get(id=id)
                    formulario = FormCamion(request.POST, instance=instancia)

                case 'Semi':
                    instancia = Semi.objects.get(id=id)
                    formulario = FormSemi(request.POST, instance=instancia)

            if(formulario and formulario.is_valid()):
                formulario.save()
                sweetify.success(request,f'{modelo} actualizado',text ='Los datos han sido actualizados correctamente', timer = 3000)

                match modelo:

                    case 'Transporte':
                        return redirect('transportes')

                    case 'Camion':
                        return redirect('camiones')

                    case 'Semi':
                        return redirect('semis')

        else:
            errores = []
            for campo, mensajes in formulario.errors.items():
                for mensaje in mensajes:
                    errores.append(f'{campo}: {mensaje}')
        
                    errores_str = '<br>'.join(errores)
                    sweetify.warning(request,'Error al editar', text = errores_str, persistent = 'Aceptar')
            return redirect('transportes')
    
    except Exception as excepcion:
        sweetify.error(request, 'Error al editar', text=f'Ocurrió un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('transportes')

