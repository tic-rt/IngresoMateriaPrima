from datetime import datetime
from django.utils import timezone
from django.shortcuts import redirect, render
import sweetify

from hdr.forms import FormHDR
from hdr.models import HDR
from porteria2.forms import FormEPP, FormEgreso, FormIngreso
from porteria2.models import Ingreso
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

@login_required
@permission_required('porteria2.view_ingreso', login_url='index')
def index(request):
    """chart de vehiculos ingresados e informacion relevante para porteria"""
    return render(request, 'porteria2/porteria2.html')

@login_required
@permission_required('porteria2.view_ingreso', login_url='index')
def nuevoIngreso(request):
    """Esta funcion devuelve un formulario de nuevo inrgeso de materia prima"""
    formulario_ingreso = FormIngreso()
    try:
        return render(request, 'porteria2/nuevoIngreso.html', {
            'formulario_ingreso': formulario_ingreso,
            # 'conductores':conductores
        })

    except Exception as excepcion:
        sweetify.error(request, title='Error', text=f'Ocurrio un error {str(excepcion)}', persistent='Aceptar')
        return render(request, 'porteria2/porteria2.html')

@login_required
@permission_required('porteria2.add_ingreso',login_url='index')
def guardarNuevoIngreso(request):
    """Esta funcion registra un nuevo ingreso de vehiculo a realizar descarga de materia prima y crea la hoja de ruta hdr"""
    # formulario_ingreso = FormIngreso()
    try:
        if request.method == 'POST':
            formulario = FormIngreso(request.POST)

            if formulario.is_valid():
                hdr = HDR()  # creando la hdr
                hdr.save()
                ingreso: Ingreso = formulario.save(commit=False)  # falta guardar
                ingreso.hdr = hdr
                ingreso.save()
                sweetify.success(request, title="Ingreso Guardado",text="Ingreso de vehiculo registrado", timer=3000)
                return redirect(f'controlEpp/?id_hdr={hdr.id}&id_ingreso={ingreso.id}')
            else:
                print(formulario.errors)
                errores = []
                for campo, mensajes in formulario.errors.items():
                    for mensaje in mensajes:
                        errores.append(f'{campo}: {mensaje}')

                errores_str = '<br>'.join(errores)
                sweetify.warning(request, title='Error al registrar Ingreso',text=errores_str, persistent='Aceptar')
                return render(request, 'porteria2/nuevoIngreso.html',
                                {'formulario_ingreso': formulario})

    except Exception as excepcion:
        sweetify.error(request, title='excepcion al registrar Ingreso', text=f'Ocurrio un error {str(excepcion)}', persistent='Aceptar')
        return render(request, 'porteria2/nuevoIngreso.html', {'formulario_ingreso': formulario})

@login_required
@permission_required('porteria2.view_epp')
def controlEpp(request):
    """esta funcion muestra el ultimo ingreso y se procede al control de epp"""
    
    try:
        if request.method =='GET':
            id_hdr = request.GET.get('id_hdr')
            id_ingreso = request.GET.get('id_ingreso')
            
            existe_id = HDR.objects.filter(id =id_hdr,is_deleted = False, estado ='Activo', sector='Porteria 2').exists()#controla si existe la hdr
            existe_ingreso = Ingreso.objects.filter(id=id_ingreso, is_deleted = False, ingresado=False).exists()#controla si existe el ingreso
        
            if(existe_id and existe_ingreso):
                #hdr = formHDR
                ingreso = Ingreso.objects.get(id = id_ingreso, is_deleted = False, ingresado = False)
                empresa_transporte = ingreso.empresa_transporte
                producto = ingreso.producto
                patente_chasis = ingreso.patente_chasis
                patente_semi = ingreso.patente_semi
                control_epp = FormEPP()
                return render(request,'porteria2/controlEpp.html',
                                {'id_hdr':id_hdr,#esto debo recibir
                                'id_ingreso':id_ingreso,
                                'empresa_transporte':empresa_transporte,
                                'producto':producto,
                                'patente_chasis':patente_chasis,
                                'patente_semi':patente_semi,
                                'form_epp':control_epp})#el post debe recibir 
            else:
                sweetify.error(request, title='Error con Ingreso o HDR', text='Ocurrio un error, no se encuentra la hoja de ruta o el ingreso referenciado', persistent = 'Aceptar')
                return redirect('nuevoIngreso')
        else:
            sweetify.error(request, title='Error con Ingreso o HDR', text='No se encuentra la hoja de ruta o el ingreso referenciado', persistent='Aceptar')
            return redirect('nuevoingreso')

    except Exception as excepcion:
        sweetify.error(request, title='Ocurrio un error', text =f'Ocurrio un error {str(excepcion)} al intentar cargar los datos', persistent = 'Aceptar')
        return redirect('nuevoIngreso')

@login_required
@permission_required('porteria2.view_epp', login_url='index')
def mostrarControlEpp(request):
    """Esta funcion devuelve una lista con todos los ingresos pendientes de control"""

    try:
        ingresos = Ingreso.objects.filter( ingresado = False, is_deleted = False, hdr__estado='Activo')
        if ingresos:
            sweetify.toast(request,  'Controles Pendientes de EPP', icon='warning', timer=3000,allowOutsideClick=False, timerProgressBar = False)
        else:
            sweetify.toast(request, 'Sin controles de EPP pendientes', icon='info', timer=3000, allowOutsideClick=False, timerProgressBar=False )
        return render(request,'porteria2/pendientes.html',
                        {'ingresos':ingresos})
    except Exception as excepcion:
        sweetify.error(request, title='Ocurrio un error', text = f'Ocurrio un error {str(excepcion)} al intentar cargar los datos', persistent = 'Aceptar')
        return redirect('nuevoIngreso')

@login_required
@permission_required('porteria2.add_epp')
def guardarControlEpp(request):
    """ esta funcion guarda un control de EPP validado, si es rechazado redirecciona  """
    try:
        if request.method == 'POST':
            form_control = FormEPP(request.POST)
            id_hdr = request.GET.get('id_hdr')
            id_ingreso = request.GET.get('id_ingreso')
            existe_id_hdr = HDR.objects.filter(id = id_hdr, is_deleted = False, estado = 'Activo',sector = 'Porteria 2').exists()
            existe_id_ingreso = Ingreso.objects.filter(id = id_ingreso, is_deleted = False, ingresado = False).exists()

            if(existe_id_hdr and existe_id_ingreso):
                hdr = HDR.objects.get(id = id_hdr, is_deleted = False, estado  = 'Activo', sector = 'Porteria 2')
                ingreso = Ingreso.objects.get(id = id_ingreso, is_deleted = False, ingresado= False)
                form_hdr = FormHDR()
                empresa_transporte = ingreso.empresa_transporte
                producto = ingreso.producto
                patente_chasis = ingreso.patente_chasis
                patente_semi = ingreso.patente_semi
                control_epp = form_control

                if form_control.is_valid():
                    casco = form_control.cleaned_data['casco']
                    mascara = form_control.cleaned_data['mascara']
                    antiparras = form_control.cleaned_data['antiparras']
                    botines = form_control.cleaned_data['botines']
                    pantalon_camisa = form_control.cleaned_data['pantalon_camisa']
                    matafuego = form_control.cleaned_data['matafuego']
                    arrestallamas = form_control.cleaned_data['arrestallamas']
                    carteleria = form_control.cleaned_data['carteleria']
                    todos = all([casco, mascara, antiparras, botines, pantalon_camisa, matafuego, arrestallamas, carteleria])

                    if todos :
                        hdr.sector = 'Almacen PQ'
                        ingreso.ingresado = True
                        ingreso.save()
                        hdr.save()
                        form_control.save()
                        sweetify.success(request, 'Control EPP', text='Se ha guardado el control de EPP', timer=3000)
                        return redirect('nuevoIngreso')
                    else:#se redirige para guardar el rechazo con el motivo 
                        sweetify.warning(request,'Control EPP', text='No se cumplen uno o mas requisitos de EPP', timer=3000)
                        #redirigir para guardar rechazo en hdr
                        return render(request,'porteria2/rechazoControlEpp.html',
                                {'empresa_transporte':empresa_transporte,
                                 'producto':producto,
                                 'patente_chasis':patente_chasis,
                                 'patente_semi':patente_semi,
                                 'id_ingreso':id_ingreso,
                                 'form_epp':control_epp,
                                 'form_hdr':form_hdr
                                 }) 
                    
                else:
                    return render(request,'porteria2/controlEpp.html',
                                {'id_hdr':id_hdr,#esto debo recibir
                                 'id_ingreso':id_ingreso,
                                 'empresa_transporte':empresa_transporte,
                                 'producto':producto,
                                 'patente_chasis':patente_chasis,
                                 'patente_semi':patente_semi,
                                 'form_epp':control_epp
                                 }) 
                    
    except Exception as excepcion:
        sweetify.error(request,'Excepcion', text=f'Hubo un problema al guardar el control {str(excepcion)}', persistent = 'Aceptar')
        return redirect ('nuevoIngreso')    

@login_required
@permission_required('hdr.change_hdr', login_url='index')
def guardarRechazo(request):
    id_ingreso = request.GET.get('id_ingreso')
    existe_id = Ingreso.objects.filter(id = id_ingreso)

    try:
        if existe_id:
            ingreso = Ingreso.objects.filter(id = id_ingreso, is_deleted = False,ingresado = False).get()
            hdr = ingreso.hdr

            if request.method == 'POST':
                form_hdr = FormHDR(request.POST, instance=hdr)
                
                if form_hdr.is_valid():
                    hdr.estado = 'Rechazado'
                    hdr.save()
                    form_hdr.save()
                    sweetify.success(request,'Rechazo de Ingreso', text =' Se ha rechazado el ingreso, la Hoja de ruta se guardo como rechazada', timer=3000)
                    return redirect('nuevoIngreso')
                else:
                    sweetify.error(request,'Error', text='Hubo un error al cargar el ingreso o HDR referenciado', persistent = 'Aceptar')
                    return redirect('nuevoIngreso')

        else:
            sweetify.error(request,'Error', text='Hubo un error al cargar el ingreso referenciado no existe', persistent = 'Aceptar')
            return redirect('nuevoIngreso')
        
    except Exception as excepcion:
        sweetify.error(request, 'Excepcion', text = f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('nuevoIngreso')

def egresosPendientes(request):
    """Esta funcion devuelve a todos los egresos pendientes"""
    
    try:
        egresos = Ingreso.objects.filter(is_deleted=False, ingresado=True, hdr__sector ='Porteria 2 E')
        if egresos:
            sweetify.toast(request, 'Egresos Pendientes', text='No hay egresos pendientes', icon='info', timer=3000, allowOutsideClick=False, timerProgressBar=False)
            return render(request,'porteria2/egresosPendientes.html',{'egresos':egresos})
        else:
            sweetify.toast(request, 'Egresos Pendientes', text='No hay egresos pendientes', icon='info', timer=3000, allowOutsideClick=False, timerProgressBar=False)
            return render(request,'porteria2/egresosPendientes.html',{'egresos':egresos})
    except Exception as excepcion:
        sweetify.error(request, 'Excepcion', text = f'Ocurrio un error {str(excepcion)}', persistent ='Aceptar')
        return redirect('nuevoIngreso')

def egreso(request):
    """Esta funcion devuelve un egreso pendiente """
    print(timezone.now())
    try:
        if request.method == 'GET':
            id_ingreso = request.GET.get('id_ingreso')

            if Ingreso.objects.filter(id=id_ingreso, is_deleted = False, ingresado=True, hdr__estado= 'Activo', hdr__sector = 'Porteria 2 E').exists():
                ingreso = Ingreso.objects.get(id=id_ingreso)
                formulario_egreso = FormEgreso(initial={'verificacion':None,'salida_autorizada':None,})
                return render(request, 'porteria2/egreso.html',{
                    'ingreso':ingreso,
                    'formulario_egreso':formulario_egreso
                    })

            else:
                sweetify.error(request,'Error', text='Hubo un error al cargar el ingreso referenciado no existe', persistent = 'Aceptar')
                return redirect('egresosPendientes')
        else:
            sweetify.error(request,'Error', text='Hubo un error al cargar el ingreso referenciado no existe', persistent = 'Aceptar')
            return redirect('egresosPendientes')
            
    except Exception as excepcion:
        sweetify.error(request,'Error', text=f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return redirect('egresosPendientes')

def guardarEgreso(request):
    """Esta funcion guarda un egreso de vehiculo"""
    try:
        if request.method == 'POST':
            formulario_egreso = FormEgreso(request.POST)
            print(formulario_egreso)
            formulario_egreso.instance.fecha_salida = datetime.now()
            id_ingreso = request.GET.get('id_ingreso')
            print(f'el id de ingreso es {id_ingreso}')
            existe_id = Ingreso.objects.filter(id = id_ingreso, is_deleted = False, ingresado = True, hdr__estado = 'Activo' ).exists()
            print(existe_id)
            
            if existe_id:
                ingreso = Ingreso.objects.get(id = id_ingreso)
                hdr = ingreso.hdr
                
                if formulario_egreso.is_valid():
                    #formulario_egreso.save()
                    hdr.sector = 'Finalizado'
                    #hdr.save()
                    sweetify.success(request,'Egreso Guardado', text=f'El egreso del vehiculo {ingreso.patente_chasis} {ingreso.patente_semi} se ha guardado', timer=3000)
                    return redirect('egresosPendientes')
                else:
                    sweetify.error(request, 'Formulario Inválido', text='Hubo un problema con el formulario, por favor revisa los campos.', persistent='Aceptar')
                    ingreso = Ingreso.objects.get(id=id_ingreso)
                    print(formulario_egreso.errors)
                    return render(request, 'porteria2/egreso.html', {'formulario_egreso': formulario_egreso,
                                                                     'ingreso': ingreso})
            else:
                sweetify.error(request, 'Error', text='El id referenciado no existe',persistent='Aceptar' )
                return redirect('egresosPendientes')
            
        else:
            return redirect('egresosPendientes')    
    except Exception as excepcion:
        print(excepcion)
        sweetify.error(request, 'Error', text=f'Ocurrio un error {str(excepcion)} ', persistent = 'Aceptar')
        return redirect('egresosPendientes')