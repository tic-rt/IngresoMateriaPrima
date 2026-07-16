import os
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required, permission_required
from IngresoMateriaPrima import settings
from balanza.models import Balanza
from laboratorio.models import Inspeccion
from pamo.models import PamoPsul
from porteria2.models import EPP, Egreso, Ingreso

# Create your views here.
@login_required
@permission_required('hdr.view_hdr', raise_exception=True)
def lista_hdr(request):
    """Funcion que devuelve la vista principal de hdr"""
    hdr = None
    try:
        hdr = Ingreso.objects.filter(ingresado = True)
    except Exception as excepcion:
        pass
    
    return render(request,'HDR/listaHDR.html',{'HDR':hdr})

@login_required
@permission_required('hdr.view_hdr', raise_exception=True)
def exportar_hdr(request):
    """esta funcion devuelve un pdf de hoja de ruta de la hdr completa"""
    id_hdr = request.GET.get('id_hdr')
    contexto = _completado(id_hdr)
    
    contexto["logo_path"] = os.path.join(
        settings.BASE_DIR,
        "app",
        "static",
        "img",
        "fmrt.jpg"
    )
    
    respuesta = HttpResponse(content_type='application/pdf')
    pisa.CreatePDF(render_to_string('HDR/HDR.html',contexto), dest=respuesta)

    return respuesta

def _completado(id_hdr):
    """funcion que devuelve todos los datos para completar la HDR"""
    contexto = {}
    contexto.update(_porteria_ingreso(id_hdr))
    contexto.update({'epp': _control_epp(id_hdr)})
    contexto.update({'balanza': _balanza(id_hdr)})
    contexto.update({'iquimica': _iquimica(id_hdr)})
    contexto.update({'pamo': _pamo(id_hdr)})
    contexto.update({'egreso': _egreso(id_hdr)})
    return contexto

def _porteria_ingreso(id_hdr):
    """funcion que trae todos los datos de la porteria 2 para la HDR"""
    existe = __existe_hdr(id_hdr, Ingreso)
    if existe:
        ingreso = Ingreso.objects.select_related(
            'empresa_transporte',
            'conductor',
            'producto',
            'patente_chasis',
            'patente_semi',
            'responsable'
            ).get(id=id_hdr)
        return {
            "fecha": ingreso.hora_ingreso,
            "calefaccion": 'SI' if ingreso.ingreso_calefaccion else 'NO',
            "empresa": ingreso.empresa_transporte.nombre,
            "conductor": str(ingreso.conductor),
            "dni": ingreso.conductor.dni,
            "producto": ingreso.producto.producto,
            "dominio": ingreso.patente_chasis.patente,
            "dominio_acomplado": ingreso.patente_semi.patente,
            "responsable_porteria": str(ingreso.responsable),
            }
    else:
        pass
            
def _control_epp(id_hdr):
    """funcion que trae todos los datos de epp para la HDR"""
    existe = __existe_hdr(id_hdr, EPP)
    
    if existe:
        epp = EPP.objects.select_related(
            'hdr'
        ).get(hdr_id=id_hdr)
        
        return {
            "fecha_control": epp.fecha_control,
            "casco": 'SI' if epp.casco else 'NO',
            "mascara": 'SI' if epp.mascara else 'NO',
            "antiparras": 'SI' if epp.antiparras else 'NO',
            "botines": 'SI' if epp.botines else 'NO',
            "pantalon_camisa": 'SI' if epp.pantalon_camisa else 'NO',
            "matafuego": 'SI' if epp.matafuego else 'NO',
            "arrestallamas": 'SI' if epp.arrestallamas else 'NO',
            "carteleria": 'SI' if epp.carteleria else 'NO',
            "responsable_epp": str(epp.responsable),
        }
    else:
        pass
    
def _balanza(id_hdr):
    """funcion que trae todos los datos de ingreso y egreso de la balanza para la HDR"""
    existe = __existe_hdr(id_hdr, Balanza)

    if existe:
        balanza = Balanza.objects.select_related(
        "proveedor",
        "hdr",
        "responsable_entrada",
        "responsable_salida"
        ).get(hdr_id=id_hdr)

        return {
            "hora_ingreso": balanza.hora_ingreso,
            "proveedor": str(balanza.proveedor),
            "remito": balanza.remito,
            "peso_origen": balanza.peso_origen,
            "responsable_entrada": str(balanza.responsable_entrada),
            "hora_salida": balanza.fecha_salida,
            "peso_fmrt": balanza.peso_fmrt,
            "peso_vacio": balanza.peso_vacio,
            "peso_taquilla": balanza.peso_taquilla,
            "peso_bolsa_tarima": balanza.peso_bolsa_tarima,
            "peso_neto": balanza.peso_neto,
            "responsable_salida": str(balanza.responsable_salida),
            }
    else:
        pass


def _iquimica(id_hdr):
    """funcion que trae todos los datos de la inspeccion quimica para la HDR"""
    existe = __existe_hdr(id_hdr, Inspeccion)
    
    if existe:
        iq = Inspeccion.objects.select_related(
        'responsable',
        'hdr'
        ).get(hdr_id=id_hdr)
    
        return {
            "fecha": iq.fecha,
            "certificado": 'SI' if iq.certificado else 'NO',
            "requisitos": 'SI' if iq.requisitos else 'NO',
            "observacion": iq.observacion,
            "responsable": str(iq.responsable),
            }
    else:
        pass
    
def _pamo(id_hdr):
    """funcion que trae todos los datos de pamo/psul para la HDR"""
    # Verificar si existe un registro de PamoPsul para la HDR dada
    existe = __existe_hdr(id_hdr, PamoPsul)
    
    if existe:
        pamo = PamoPsul.objects.select_related(
        'responsable',
        'hdr'
        ).get(hdr_id=id_hdr)
    
        producto = _producto(id_hdr)
        

        if producto == 'Azufre Líquido' or producto == 'Amoníaco':
            return {
                "producto": producto,
                "hora_ingreso": pamo.hora_ingreso,
                "presion_ingreso": pamo.presion_ingreso,
                "temperatura_ingreso": pamo.temperatura_ingreso,
                "presion_salida": pamo.presion_salida,
                "temperatura_salida": pamo.temperatura_salida,
                "hora_salida": pamo.hora_salida,
                "responsable": str(pamo.responsable),
                }
        else:
            return {
                "producto": "No corresponde",
                "hora_ingreso": None,    
                "hora_salida": None,
                "presion_ingreso": None,
                "temperatura_ingreso": None,
                "presion_salida": None,
                "temperatura_salida": None,
                "responsable": str(pamo.responsable),
                }
    else:
        pass
        
def _egreso(id_hdr):
    """funcion que trae todos los datos de egreso de la porteria 2 para la HDR"""
    existe = __existe_hdr(id_hdr, Egreso)
    
    if existe:
        egreso = Egreso.objects.select_related(
        'responsable',
        'hdr'
        ).get(hdr_id=id_hdr)

        return {
            "fecha_salida": egreso.fecha_salida,
            "verificacion": 'SI' if egreso.verificacion else 'NO',
            "salida_autorizada": 'SI' if egreso.salida_autorizada else 'NO',
            "responsable": str(egreso.responsable),
            }
    else:
        pass

def _producto(id_hdr):
    """funcion que trae el producto de la hdr"""
    
    ingreso = Ingreso.objects.select_related(
        'producto',
        'hdr'
    ).get(hdr_id=id_hdr)

    return ingreso.producto.producto

def __existe_hdr(id_hdr,objeto):
    """funcion que verifica si existe una hdr del objeto dado"""
    clase = objeto
    return clase.objects.filter(id=id_hdr).exists()