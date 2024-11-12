from datetime import date
from django.shortcuts import redirect, render
import sweetify

from hdr.models import HDR
from porteria2.forms import FormIngreso
from porteria2.models import Ingreso
from transporte.models import Camion, Conductor, Semi

# Create your views here.

def index(request):
    """chart de vehiculos ingresados e informacion relevante para porteria"""
    return render(request,'porteria2/porteria2.html')

def nuevoIngreso(request):
    """Esta funcion devuelve un formulario de nuevo inrgeso de materia prima"""
    formulario_ingreso = FormIngreso()
    try:
        return render(request,'porteria2/nuevoIngreso.html',{
            'formulario_ingreso':formulario_ingreso,
            #'conductores':conductores
                    })
        
    except Exception as excepcion:
        sweetify.error(request, title='Error', text=f'Ocurrio un error {str(excepcion)}', persistent='Aceptar')
        return render(request, 'porteria2/porteria2.html')

def guardarNuevoIngreso(request):
    """Esta funcion registra un nuevo ingreso de vehiculo a realizar descarga de materia prima y crea la hoja de ruta hdr"""
    #formulario_ingreso = FormIngreso()
    try:
        if request.method == 'POST':
            formulario = FormIngreso(request.POST)
                
            if formulario.is_valid():
                hdr = HDR()
                #hdr.save()
                id_hdr = hdr.id
                ingreso : Ingreso = formulario.save(commit=False)#falta guardar
                ingreso.id_hdr = id_hdr
                sweetify.success(request,title="Ingreso Guardado",text="Ingreso de vehiculo registrado", timer=3000)
                return redirect('nuevoIngreso')
            else:
                print(formulario.errors)
                errores = []
                for campo, mensajes in formulario.errors.items():
                    for mensaje in mensajes:
                        errores.append(f'{campo}: {mensaje}')

                errores_str ='<br>'.join(errores)
                sweetify.warning(request,title='Error al registrar Ingreso', text=errores_str, persistent = 'Aceptar')
                return render(request,'porteria2/nuevoIngreso.html',
                              {'formulario_ingreso':formulario})

    except Exception as excepcion:
        sweetify.error(request, 'excepcion al registrar Ingreso', text =f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return render(request,'porteria2/nuevoIngreso.html',
                              {'formulario_ingreso':formulario})
    

def guardarNuevoIngreso2(request):
    """Esta funcion registra un nuevo ingreso de vehiculo a realizar descarga de materia prima y crea la hoja de ruta hdr"""
    #formulario_ingreso = FormIngreso()
    try:
        if request.method == 'POST':
            formulario_data = request.POST.copy()
            print(f'Lo que viene es  `\n` {formulario_data}')
            formulario = FormIngreso(formulario_data)
            print(f'convertido a FormIngreso`\n {formulario} `\n`')

        
            # Ver los valores de cada campo específico
            print('Empresa ID:',formulario.data.get('empresa_transporte')) # ver el id de empresa
            print("Conductor ID:", formulario.data.get('conductor'))  # Ver el conductor
            print("Patente Chasis ID:", formulario.data.get('patente_chasis'))  # Ver el camion
            print("Patente Semi ID:", formulario.data.get('patente_semi'))  # Ver el semi
            print("Responsable ID",formulario.data.get('responsable'))
            print('----------------')
            print('Conductor:', Conductor.objects.filter(id=formulario.data.get('conductor')).exists())
            print('Camion:', Camion.objects.filter(id=formulario.data.get('patente_chasis')).exists())
            print('Semi:', Semi.objects.filter(id=formulario.data.get('patente_semi')).exists())
            print('----------------')
            
            # Imprimir los datos recibidos para depuración
            print('Formulario POST data:', request.POST)
            id_conductor = formulario.data.get('conductor')
            id_empresa = formulario.data.get('empresa_transporte')
            print(f'el id de conductor es un numero? {isinstance(id_conductor,int)}')
            print(f'el id de empresa es un numero? {isinstance(id_empresa,int)}')

            empresa_id = formulario_data.get('empresa_transporte')
            if empresa_id:
                formulario.fields['conductor'].queryset = Conductor.objects.filter(transporte_id=empresa_id)
                formulario.fields['patente_chasis'].queryset = Camion.objects.filter(transporte_id=empresa_id)
                formulario.fields['patente_semi'].queryset = Semi.objects.filter(transporte_id=empresa_id)
                
            if formulario.is_valid():
                hdr = HDR()
                #hdr.save()
                id_hdr = hdr.id
                ingreso : Ingreso = formulario.save(commit=False)#falta guardar
                ingreso.id_hdr = id_hdr
                sweetify.success(request,title="Ingreso Guardado",text="Ingreso de vehiculo registrado", timer=3000)
                return redirect('nuevoIngreso')
            else:
                print(formulario.errors)
                errores = []
                for campo, mensajes in formulario.errors.items():
                    for mensaje in mensajes:
                        errores.append(f'{campo}: {mensaje}')

                errores_str ='<br>'.join(errores)
                sweetify.warning(request,title='Error al registrar Ingreso', text=errores_str, persistent = 'Aceptar')
                return render(request,'porteria2/nuevoIngreso.html',
                              {'formulario_ingreso':formulario})

    except Exception as excepcion:
        sweetify.error(request, 'excepcion al registrar Ingreso', text =f'Ocurrio un error {str(excepcion)}', persistent = 'Aceptar')
        return render(request,'porteria2/nuevoIngreso.html',
                              {'formulario_ingreso':formulario})