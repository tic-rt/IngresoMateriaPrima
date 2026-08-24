import os
import django
from datetime import date, timedelta, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IngresoMateriaPrima.settings')
django.setup()

from hdr.models import HDR
from personal.models import Personal
from transporte.models import Transporte, Camion, Semi, Conductor
from proveedores.models import Proveedor, Producto, ProveedorProducto
from porteria2.models import Ingreso, EPP
from balanza.models import Balanza
from laboratorio.models import Inspeccion
from pamo.models import PamoPsul
from calidad.models import Calidad


def get_or_create_pp(proveedor, producto):
    """Crea la relacion proveedor-producto si no existe"""
    pp, _ = ProveedorProducto.objects.get_or_create(
        proveedor=proveedor,
        producto=producto,
    )
    return pp


def crear_ingreso(hdr, transporte, conductor, camion, semi, producto, remito, responsable,
                  laborable=True, con_epp=True, ingresado=True):
    """Crea un ingreso con su control de EPP"""
    ingreso = Ingreso.objects.create(
        ingreso_calefaccion=False,
        empresa_transporte=transporte,
        conductor=conductor,
        producto=producto,
        remito=remito,
        patente_chasis=camion,
        patente_semi=semi,
        responsable=responsable,
        ingresado=ingresado,
        laborable=laborable,
        hdr=hdr,
    )
    if con_epp:
        personal_porteria = Personal.objects.filter(sector='Porteria 2').first()
        EPP.objects.create(
            casco=True,
            mascara=True,
            antiparras=True,
            botines=True,
            pantalon_camisa=True,
            matafuego=True,
            arrestallamas=True,
            carteleria=True,
            responsable=responsable if responsable.sector == 'Porteria 2' else personal_porteria,
            hdr=hdr,
        )
    return ingreso


def main():
    print('=== Sembrando datos de ejemplo para el manual ===')

    # ---- Obtener o crear personal por sector ----
    personal_porteria = Personal.objects.get(sector='Porteria 2')
    personal_iq = Personal.objects.get(sector='Inspeccion Quimica')
    personal_almacen = Personal.objects.get(sector='Almacen PQ')
    personal_shyma = Personal.objects.get(sector='SHYMA')
    personal_pamo = Personal.objects.get(sector='PAMO')
    personal_psul = Personal.objects.get(sector='PSUL')

    # ---- Transporte ----
    transporte1 = Transporte.objects.get(nombre='Transporte del Sur')
    transporte2 = Transporte.objects.get(nombre='Cargas del Norte')
    transporte3 = Transporte.objects.get(nombre='Logistica Central')

    camion1 = Camion.objects.get(patente='AA100AA')
    semi1 = Semi.objects.get(patente='AA101AA')
    camion2 = Camion.objects.get(patente='BB100BB')
    semi2 = Semi.objects.get(patente='BB101BB')
    camion3 = Camion.objects.get(patente='CC100CC')
    semi3 = Semi.objects.get(patente='CC101CC')

    conductor1 = Conductor.objects.get(dni='20256654')
    conductor2 = Conductor.objects.get(dni='28123456')
    conductor3 = Conductor.objects.get(dni='27123456')

    # ---- Productos ----
    azufre_liquido = Producto.objects.get(producto='Azufre Líquido')
    azufre_solido = Producto.objects.get(producto='Azufre sólido')
    amoniaco = Producto.objects.get(producto='Amoníaco')
    hipoclorito = Producto.objects.get(producto='Hipoclorito')

    # ---- Proveedores ----
    proveedor1 = Proveedor.objects.get(nombre='YPF')
    proveedor2 = Proveedor.objects.get(nombre='Petroquimica Sur')
    proveedor3 = Proveedor.objects.get(nombre='Quimica del Valle')
    proveedor4 = Proveedor.objects.get(nombre='Agroinsumos SA')

    # Relaciones proveedor-producto
    get_or_create_pp(proveedor1, azufre_liquido)
    get_or_create_pp(proveedor1, azufre_solido)
    get_or_create_pp(proveedor2, amoniaco)
    get_or_create_pp(proveedor3, hipoclorito)
    get_or_create_pp(proveedor4, azufre_liquido)

    # ============================================================
    # 1. PORTERIA 2 - Ingresos pendientes de control EPP
    #    (ingresado=False, hdr sector 'Porteria 2', estado 'Activo')
    # ============================================================
    for i in range(1, 3):
        hdr = HDR.objects.create(sector='Porteria 2', estado='Activo')
        crear_ingreso(
            hdr=hdr,
            transporte=transporte1 if i == 1 else transporte2,
            conductor=conductor1 if i == 1 else conductor2,
            camion=camion1 if i == 1 else camion2,
            semi=semi1 if i == 1 else semi2,
            producto=azufre_liquido if i == 1 else amoniaco,
            remito=f'R-{1000 + i}',
            responsable=personal_porteria,
            ingresado=False,
            con_epp=False,
        )
    print('Porteria 2: 2 ingresos pendientes de control EPP creados')

    # ============================================================
    # 2. BALANZA - Ingresos pendientes de pesaje (entrada)
    #    (ingresado=True, hdr sector 'Almacen PQ')
    # ============================================================
    for i in range(1, 3):
        hdr = HDR.objects.create(sector='Almacen PQ', estado='Activo')
        personal_resp = personal_porteria if i == 1 else personal_porteria
        crear_ingreso(
            hdr=hdr,
            transporte=transporte1 if i == 1 else transporte3,
            conductor=conductor1 if i == 1 else conductor3,
            camion=camion1 if i == 1 else camion3,
            semi=semi1 if i == 1 else semi3,
            producto=azufre_solido if i == 1 else hipoclorito,
            remito=f'R-{2000 + i}',
            responsable=personal_resp,
            con_epp=True,
        )
    print('Balanza: 2 ingresos pendientes de pesaje de entrada creados')

    # ============================================================
    # 3. INSPECCION QUIMICA - Pendientes de inspeccion (laborable)
    #    (hdr sector 'Inspeccion PQ', pesaje de entrada ya hecho)
    # ============================================================
    for i in range(1, 3):
        hdr = HDR.objects.create(sector='Inspeccion PQ', estado='Activo')
        ingreso = crear_ingreso(
            hdr=hdr,
            transporte=transporte2 if i == 1 else transporte1,
            conductor=conductor2 if i == 1 else conductor1,
            camion=camion2 if i == 1 else camion1,
            semi=semi2 if i == 1 else semi1,
            producto=azufre_liquido if i == 1 else amoniaco,
            remito=f'R-{3000 + i}',
            responsable=personal_porteria,
            con_epp=True,
        )
        # Pesaje de entrada
        Balanza.objects.create(
            hora_ingreso=__import__('django.utils.timezone', fromlist=['now']).now() - timedelta(hours=2),
            proveedor=proveedor1 if i == 1 else proveedor2,
            remito=ingreso.remito,
            peso_origen=25000,
            responsable_entrada=personal_almacen,
            observaciones='DOD según el IN 11-IQ-07',
            hdr=hdr,
        )
    print('Inspeccion Quimica: 2 ingresos pendientes de inspeccion creados')

    # ============================================================
    # 4. IQ - Control de dias no laborables (inspeccion pendiente)
    #    (laborable=False, inspeccion cerrado=False, hdr sector 'Almacen PQ E')
    # ============================================================
    hdr = HDR.objects.create(sector='Almacen PQ E', estado='Activo')
    ingreso = crear_ingreso(
        hdr=hdr,
        transporte=transporte3,
        conductor=conductor3,
        camion=camion3,
        semi=semi3,
        producto=azufre_solido,
        remito='R-4001',
        responsable=personal_porteria,
        laborable=False,
        con_epp=True,
    )
    Balanza.objects.create(
        hora_ingreso=__import__('django.utils.timezone', fromlist=['now']).now() - timedelta(hours=3),
        proveedor=proveedor4,
        remito=ingreso.remito,
        peso_origen=22000,
        responsable_entrada=personal_almacen,
        observaciones='DOD según el IN 11-IQ-07',
        hdr=hdr,
    )
    # Inspeccion sin cerrar (pendiente de control)
    Inspeccion.objects.create(
        certificado=False,
        requisitos=False,
        descargar=False,
        responsable=personal_iq,
        observacion='',
        cerrado=False,
        hdr=hdr,
    )
    print('Inspeccion Quimica: 1 ingreso pendiente de control dia no laborable creado')

    # ============================================================
    # 5. PAMO - Pendientes de control de presion/temperatura
    #    (hdr sector 'PAMO', inspeccion cerrada=True)
    # ============================================================
    hdr = HDR.objects.create(sector='PAMO', estado='Activo')
    ingreso = crear_ingreso(
        hdr=hdr,
        transporte=transporte2,
        conductor=conductor2,
        camion=camion2,
        semi=semi2,
        producto=amoniaco,
        remito='R-5001',
        responsable=personal_porteria,
        con_epp=True,
    )
    Balanza.objects.create(
        hora_ingreso=__import__('django.utils.timezone', fromlist=['now']).now() - timedelta(hours=4),
        proveedor=proveedor2,
        remito=ingreso.remito,
        peso_origen=18000,
        responsable_entrada=personal_almacen,
        observaciones='DOD según el IN 11-IQ-07',
        hdr=hdr,
    )
    Inspeccion.objects.create(
        certificado=True,
        requisitos=True,
        descargar=True,
        responsable=personal_iq,
        observacion='Certificado OK',
        cerrado=True,
        hdr=hdr,
    )
    print('PAMO: 1 ingreso pendiente de control creado')

    # ============================================================
    # 6. PSUL - Pendientes de control de presion/temperatura
    #    (hdr sector 'PSUL', inspeccion cerrada=True)
    # ============================================================
    hdr = HDR.objects.create(sector='PSUL', estado='Activo')
    ingreso = crear_ingreso(
        hdr=hdr,
        transporte=transporte1,
        conductor=conductor1,
        camion=camion1,
        semi=semi1,
        producto=azufre_liquido,
        remito='R-6001',
        responsable=personal_porteria,
        con_epp=True,
    )
    Balanza.objects.create(
        hora_ingreso=__import__('django.utils.timezone', fromlist=['now']).now() - timedelta(hours=5),
        proveedor=proveedor1,
        remito=ingreso.remito,
        peso_origen=20000,
        responsable_entrada=personal_almacen,
        observaciones='DOD según el IN 11-IQ-07',
        hdr=hdr,
    )
    Inspeccion.objects.create(
        certificado=True,
        requisitos=True,
        descargar=True,
        responsable=personal_iq,
        observacion='Azufre liquido OK',
        cerrado=True,
        hdr=hdr,
    )
    print('PSUL: 1 ingreso pendiente de control creado')

    # ============================================================
    # 7. BALANZA - Egresos pendientes de pesaje de salida
    #    (hdr sector 'Almacen PQ E')
    # ============================================================
    for i in range(1, 3):
        hdr = HDR.objects.create(sector='Almacen PQ E', estado='Activo')
        ingreso = crear_ingreso(
            hdr=hdr,
            transporte=transporte3 if i == 1 else transporte2,
            conductor=conductor3 if i == 1 else conductor2,
            camion=camion3 if i == 1 else camion2,
            semi=semi3 if i == 1 else semi2,
            producto=hipoclorito if i == 1 else azufre_solido,
            remito=f'R-{7000 + i}',
            responsable=personal_porteria,
            con_epp=True,
        )
        Balanza.objects.create(
            hora_ingreso=__import__('django.utils.timezone', fromlist=['now']).now() - timedelta(hours=6),
            proveedor=proveedor3 if i == 1 else proveedor4,
            remito=ingreso.remito,
            peso_origen=25000,
            responsable_entrada=personal_almacen,
            observaciones='DOD según el IN 11-IQ-07',
            hdr=hdr,
        )
        Inspeccion.objects.create(
            certificado=True,
            requisitos=True,
            descargar=True,
            responsable=personal_iq,
            observacion='Listo para descarga',
            cerrado=True,
            hdr=hdr,
        )
        # Control PAMO o PSUL completado
        if i == 1:
            PamoPsul.objects.create(
                hora_ingreso=time(8, 0),
                presion_ingreso=2.5,
                temperatura_ingreso=20.0,
                presion_salida=2.4,
                temperatura_salida=21.0,
                hora_salida=time(9, 30),
                responsable=personal_pamo,
                hdr=hdr,
            )
        else:
            PamoPsul.objects.create(
                hora_ingreso=time(8, 30),
                presion_ingreso=1.8,
                temperatura_ingreso=22.5,
                presion_salida=1.7,
                temperatura_salida=23.0,
                hora_salida=time(10, 0),
                responsable=personal_psul,
                hdr=hdr,
            )
    print('Balanza: 2 ingresos pendientes de pesaje de salida creados')

    # ============================================================
    # 8. PORTERIA 2 - Egresos pendientes
    #    (hdr sector 'Porteria 2 E', estado 'Activo' o 'RechazoConfirmado')
    # ============================================================
    for i in range(1, 3):
        estado = 'Activo' if i == 1 else 'RechazoConfirmado'
        hdr = HDR.objects.create(sector='Porteria 2 E', estado=estado)
        crear_ingreso(
            hdr=hdr,
            transporte=transporte1 if i == 1 else transporte3,
            conductor=conductor1 if i == 1 else conductor3,
            camion=camion1 if i == 1 else camion3,
            semi=semi1 if i == 1 else semi3,
            producto=azufre_liquido if i == 1 else amoniaco,
            remito=f'R-{8000 + i}',
            responsable=personal_porteria,
            con_epp=True,
        )
    print('Porteria 2: 2 egresos pendientes creados')

    # ============================================================
    # 9. CALIDAD - Registros de calidad
    # ============================================================
    calidad_data = [
        {'fecha_vigencia': date.today() + timedelta(days=30), 'version': 3, 'registro': 'IN 11-IQ-07'},
        {'fecha_vigencia': date.today() + timedelta(days=60), 'version': 2, 'registro': 'IN 11-PQ-02'},
        {'fecha_vigencia': date.today() + timedelta(days=90), 'version': 1, 'registro': 'IN 11-BL-01'},
        {'fecha_vigencia': date.today() + timedelta(days=120), 'version': 4, 'registro': 'IN 11-SH-03'},
    ]
    for c in calidad_data:
        Calidad.objects.get_or_create(
            registro=c['registro'],
            defaults={'fecha_vigencia': c['fecha_vigencia'], 'version': c['version']},
        )
    print('Calidad: 4 registros creados')

    print('=== SEED COMPLETADO ===')


if __name__ == '__main__':
    main()