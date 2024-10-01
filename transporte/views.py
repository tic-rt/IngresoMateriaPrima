from django.http import HttpResponse
from django.shortcuts import redirect, render

from transporte.forms import FormCamion, FormSemi, FormTransporte
from transporte.models import Camion, Semi, Transporte
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
    
    camiones = Camion.objects.all()

    form_camion = FormCamion()

    return render(request,'transporte/camiones.html', 
                  {'camiones':camiones,
                   'form_camion':form_camion
                   })

def semis(request):
    """Esta funcion devolvera todos los semis de transportes registradas junto a los formularios correspondientes para la carga"""
    
    semis = Semi.objects.all()

    form_semi = FormSemi()

    return render(request,'transporte/semis.html', 
                  {'semis':semis,
                   'form_semi': form_semi
                   })


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
    print('me llamaron desde afuera para guardar un semi')

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
    
def eliminarTransporte(request):
    """Esta funcion elimina una empresa de transporte por su id   print('entrando a eliminar')"""

    try:
        if request.method == 'POST':
            
            idEmpresa = request.POST.get('id')

            if Transporte.objects.filter(id=idEmpresa, is_deleted=False).exists():  # si no existe lanza la excepcion
                transporte = Transporte.objects.get(id=idEmpresa)
                #transporte.delete()  # Eliminar el transporte
                sweetify.success(request, 'Empresa Eliminada', text=f'La empresa {transporte.nombre} ha sido eliminada', timer = 3000)
                print('eliminado')
                return redirect('transportes')
            else:
                sweetify.warning(request, 'No permitido', text='La empresa no existe o ya fue eliminada')
                print('no eliminado')
                return redirect('transportes')
            
    except Transporte.DoesNotExist as excepcion:
        sweetify.error(request, 'Error al eliminar', text='La empresa que intentas eliminar no existe o no se encuentra', persistent='Si crees que es un error, comunicate con sistemas')
        return redirect('transportes')
    
    except Exception as excepcion:
        sweetify.error(request, 'Error al eliminar', text=f'Ocurrió un error {str(excepcion)}')
        return redirect('transportes')
    