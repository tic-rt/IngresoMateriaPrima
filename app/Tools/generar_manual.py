import os
import base64
import tempfile
from playwright.sync_api import sync_playwright

OUTPUT_DIR = 'manuales'
CAPTURAS_DIR = 'capturas'
HTML_DIR = 'manuales_html'


def img_base64(nombre):
    """Convierte una imagen PNG a base64 para embederla en HTML"""
    ruta = os.path.join(CAPTURAS_DIR, nombre)
    with open(ruta, 'rb') as f:
        data = f.read()
    return 'data:image/png;base64,' + base64.b64encode(data).decode()


def img_html(nombre, alt=''):
    """Genera la etiqueta img con la imagen en base64"""
    src = img_base64(nombre)
    return '<img src="' + src + '" alt="' + alt + '" style="max-width:100%; border:1px solid #ccc; border-radius:8px; margin:10px 0;">'


CSS_BASE = """
@page {
    size: A4;
    margin: 2cm 1.5cm;
    @bottom-center {
        content: "Manual de Usuario - Ingreso de Materia Prima";
        font-size: 8pt;
        color: #666;
    }
    @bottom-right {
        content: counter(page);
        font-size: 8pt;
        color: #666;
    }
}
body {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
    color: #333;
    line-height: 1.5;
}
h1 {
    color: #0d6e8a;
    border-bottom: 3px solid #0d6e8a;
    padding-bottom: 5px;
    page-break-after: avoid;
}
h2 {
    color: #0d6e8a;
    margin-top: 20px;
    page-break-after: avoid;
}
h3 {
    color: #0d6e8a;
    margin-top: 15px;
}
.captura {
    text-align: center;
    margin: 10px 0;
}
.captura img {
    max-width: 100%;
    border: 1px solid #ccc;
    border-radius: 8px;
}
.captura p {
    font-size: 9pt;
    color: #666;
    font-style: italic;
    margin-top: 5px;
}
.pasos {
    background: #f8f9fa;
    border-left: 4px solid #0d6e8a;
    padding: 10px 15px;
    margin: 10px 0;
    border-radius: 0 8px 8px 0;
}
.pasos ol {
    margin: 0;
    padding-left: 20px;
}
.pasos li {
    margin-bottom: 5px;
}
.nota {
    background: #fff3cd;
    border: 1px solid #ffc107;
    border-radius: 8px;
    padding: 10px 15px;
    margin: 10px 0;
}
.advertencia {
    background: #f8d7da;
    border: 1px solid #dc3545;
    border-radius: 8px;
    padding: 10px 15px;
    margin: 10px 0;
}
.tabla-info {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
}
.tabla-info th {
    background: #0d6e8a;
    color: white;
    padding: 8px;
    text-align: left;
}
.tabla-info td {
    border: 1px solid #dee2e6;
    padding: 8px;
}
.tabla-info tr:nth-child(even) {
    background: #f8f9fa;
}
.portada {
    text-align: center;
    padding: 100px 0;
    page-break-after: always;
}
.portada h1 {
    font-size: 24pt;
    color: #0d6e8a;
    border: none;
}
.portada .subtitulo {
    font-size: 16pt;
    color: #666;
}
.portada .modulo {
    font-size: 20pt;
    color: #0d6e8a;
    margin-top: 30px;
}
"""


def generar_html_sector(titulo, contenido):
    """Genera un HTML completo para un sector"""
    html = '<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="UTF-8">\n'
    html += '<style>' + CSS_BASE + '</style>\n</head>\n<body>\n'
    html += '<div class="portada">\n'
    html += '<h1>Manual de Usuario</h1>\n'
    html += '<div class="subtitulo">Sistema de Ingreso de Materia Prima</div>\n'
    html += '<div class="modulo">' + titulo + '</div>\n'
    html += '</div>\n'
    html += contenido
    html += '\n</body>\n</html>'
    return html


def generar_pdf(html, nombre_archivo):
    """Convierte HTML a PDF usando la impresion de Playwright (Chromium)"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ruta = os.path.join(OUTPUT_DIR, nombre_archivo)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until='networkidle')
        page.pdf(path=ruta, format='A4', print_background=True,
                 margin={'top': '20mm', 'bottom': '20mm', 'left': '15mm', 'right': '15mm'})
        browser.close()
    print('  PDF generado: ' + ruta)


def guardar_html(html, nombre_archivo):
    """Guarda el HTML en el directorio manuales_html/ para revision y edicion"""
    os.makedirs(HTML_DIR, exist_ok=True)
    ruta = os.path.join(HTML_DIR, nombre_archivo)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(html)
    print('  HTML guardado: ' + ruta)


# ============================================================
# CONTENIDO DE CADA SECTOR
# ============================================================

def contenido_porteria():
    c = '<h1>1. Porteria 2</h1>\n'
    c += '<p>El modulo de <strong>Porteria 2</strong> es el punto de entrada de los camiones que ingresan a la planta para descargar materia prima. Aqui se registra el ingreso del vehiculo, se realiza el control de Elementos de Proteccion Personal (EPP) y se gestiona el egreso del camion al finalizar el circuito.</p>\n'
    c += '<h2>1.1 Dashboard de Porteria</h2>\n'
    c += '<p>Al ingresar al modulo de Porteria se muestra un panel con estadisticas de los ingresos realizados, vehiculos en transito, rechazados y finalizados.</p>\n'
    c += '<div class="captura">\n' + img_html('porteria_dashboard.png') + '\n<p>Figura 1: Dashboard de Porteria 2</p>\n</div>\n'
    c += '<h2>1.2 Nuevo Ingreso de Vehiculo</h2>\n'
    c += '<p>Para registrar la llegada de un camion a la planta, se debe completar el formulario de nuevo ingreso con los siguientes datos:</p>\n'
    c += '<div class="pasos">\n<ol>\n'
    c += '<li>Seleccionar la <strong>empresa de transporte</strong>.</li>\n'
    c += '<li>Seleccionar el <strong>conductor</strong> (solo se muestran conductores con carnet vigente).</li>\n'
    c += '<li>Seleccionar la <strong>patente del chasis</strong> (solo camiones con seguro vigente).</li>\n'
    c += '<li>Seleccionar la <strong>patente del semi</strong> (solo semis con seguro vigente).</li>\n'
    c += '<li>Ingresar el <strong>numero de remito</strong>.</li>\n'
    c += '<li>Seleccionar el <strong>producto</strong> a descargar.</li>\n'
    c += '<li>Indicar si el ingreso es para <strong>calefaccion de cisterna</strong>.</li>\n'
    c += '<li>Indicar si <strong>personal de Inspeccion Quimica se encuentra presente</strong> (seleccionar "No" en feriados o asuetos).</li>\n'
    c += '<li>Seleccionar el <strong>responsable</strong> de Porteria 2.</li>\n'
    c += '<li>Hacer clic en <strong>Guardar</strong>.</li>\n'
    c += '</ol>\n</div>\n'
    c += '<div class="captura">\n' + img_html('porteria_nuevo_ingreso.png') + '\n<p>Figura 2: Formulario de Nuevo Ingreso</p>\n</div>\n'
    c += '<h2>1.3 Control de EPP</h2>\n'
    c += '<p>Despues de registrar el ingreso, se debe realizar el control de Elementos de Proteccion Personal del conductor. Se verifican los siguientes elementos:</p>\n'
    c += '<ul>\n'
    c += '<li><strong>Casco</strong></li>\n'
    c += '<li><strong>Mascara</strong></li>\n'
    c += '<li><strong>Antiparras PVC</strong></li>\n'
    c += '<li><strong>Botines</strong></li>\n'
    c += '<li><strong>Pantalon/Camisa/Mameluco anti-acido</strong></li>\n'
    c += '<li><strong>Matafuego</strong></li>\n'
    c += '<li><strong>Arresta llamas</strong></li>\n'
    c += '<li><strong>Carteleria</strong></li>\n'
    c += '</ul>\n'
    c += '<div class="pasos">\n<ol>\n'
    c += '<li>Verificar cada elemento marcando la casilla correspondiente.</li>\n'
    c += '<li>Seleccionar el <strong>responsable</strong> del control.</li>\n'
    c += '<li>Si todos los elementos estan marcados, el sistema muestra el mensaje "Se cumplen todos los requisitos de EPP necesarios".</li>\n'
    c += '<li>Hacer clic en <strong>Guardar Control</strong>.</li>\n'
    c += '</ol>\n</div>\n'
    c += '<div class="captura">\n' + img_html('porteria_control_epp.png') + '\n<p>Figura 3: Control de EPP</p>\n</div>\n'
    c += '<div class="advertencia">\n<strong>Importante:</strong> Si uno o varios elementos no son marcados, el ingreso sera guardado como rechazado. Se debe indicar el motivo del rechazo.\n</div>\n'
    c += '<h2>1.4 Controles EPP Pendientes</h2>\n'
    c += '<p>Esta pantalla muestra todos los ingresos que aun no han pasado por el control de EPP. Al hacer clic en una fila, se accede al formulario de control.</p>\n'
    c += '<div class="captura">\n' + img_html('porteria_controles_epp_pendientes.png') + '\n<p>Figura 4: Controles de EPP pendientes</p>\n</div>\n'
    c += '<h2>1.5 Egresos Pendientes</h2>\n'
    c += '<p>Al finalizar el circuito, el camion regresa a Porteria 2 para su egreso. Esta pantalla muestra los vehiculos que estan listos para salir.</p>\n'
    c += '<div class="captura">\n' + img_html('porteria_egresos_pendientes.png') + '\n<p>Figura 5: Egresos pendientes</p>\n</div>\n'
    c += '<h2>1.6 Registro de Egreso</h2>\n'
    c += '<div class="pasos">\n<ol>\n'
    c += '<li>Seleccionar si se realizo la <strong>verificacion del vehiculo/carga</strong>.</li>\n'
    c += '<li>Indicar si la <strong>salida esta autorizada</strong>.</li>\n'
    c += '<li>Seleccionar el <strong>responsable</strong> del egreso.</li>\n'
    c += '<li>Hacer clic en <strong>Guardar</strong>.</li>\n'
    c += '</ol>\n</div>\n'
    c += '<div class="captura">\n' + img_html('porteria_egreso.png') + '\n<p>Figura 6: Registro de Egreso</p>\n</div>\n'
    return c


def contenido_balanza():
    c = '<h1>2. Balanza</h1>\n'
    c += '<p>El modulo de <strong>Balanza</strong> registra el peso de los camiones a la entrada y a la salida de la planta. Se realiza el pesaje de entrada cuando el camion llega con la materia prima y el pesaje de salida cuando el camion egresa despues de la descarga.</p>\n'
    c += '<h2>2.1 Inicio de Balanza</h2>\n'
    c += '<p>Pantalla principal del modulo de Balanza con acceso a las funciones de pesaje.</p>\n'
    c += '<div class="captura">\n' + img_html('balanza_inicio.png') + '\n<p>Figura 1: Inicio de Balanza</p>\n</div>\n'
    c += '<h2>2.2 Ingresos Pendientes de Pesaje</h2>\n'
    c += '<p>Muestra los camiones que han sido autorizados por Porteria 2 y estan listos para el pesaje de entrada.</p>\n'
    c += '<div class="captura">\n' + img_html('balanza_pendientes.png') + '\n<p>Figura 2: Ingresos pendientes de pesaje</p>\n</div>\n'
    c += '<h2>2.3 Pesaje de Entrada</h2>\n'
    c += '<p>Al seleccionar un camion pendiente, se carga el formulario de pesaje de entrada con los siguientes campos:</p>\n'
    c += '<div class="pasos">\n<ol>\n'
    c += '<li>Verificar el <strong>remito</strong> (si hay inconsistencia, verificar con Porteria 2).</li>\n'
    c += '<li>Seleccionar el <strong>proveedor</strong>.</li>\n'
    c += '<li>Ingresar el <strong>peso de origen</strong> en kilogramos.</li>\n'
    c += '<li>Completar las <strong>observaciones</strong> (ej: DOD segun el IN 11-IQ-07).</li>\n'
    c += '<li>Seleccionar el <strong>responsable de entrada</strong>.</li>\n'
    c += '<li>Hacer clic en <strong>Guardar pesaje</strong>.</li>\n'
    c += '</ol>\n</div>\n'
    c += '<div class="captura">\n' + img_html('balanza_pesaje_entrada.png') + '\n<p>Figura 3: Pesaje de entrada</p>\n</div>\n'
    c += '<h2>2.4 Egresos (Pesaje de Salida)</h2>\n'
    c += '<p>Muestra los camiones que han completado la descarga y estan listos para el pesaje de salida.</p>\n'
    c += '<div class="captura">\n' + img_html('balanza_egresos.png') + '\n<p>Figura 4: Egresos pendientes de pesaje de salida</p>\n</div>\n'
    c += '<h2>2.5 Pesaje de Salida</h2>\n'
    c += '<p>Al seleccionar un camion para el pesaje de salida, se cargan los siguientes campos:</p>\n'
    c += '<div class="pasos">\n<ol>\n'
    c += '<li>Verificar la <strong>fecha de salida</strong> (se completa automaticamente).</li>\n'
    c += '<li>Ingresar el <strong>peso en FMRT</strong> (peso bruto en la balanza de la planta).</li>\n'
    c += '<li>Ingresar el <strong>peso vacio</strong> del camion.</li>\n'
    c += '<li>Ingresar el <strong>peso de taquilla</strong>.</li>\n'
    c += '<li>Ingresar el <strong>peso de bolsa/tarima</strong>.</li>\n'
    c += '<li>El <strong>peso neto</strong> se calcula automaticamente.</li>\n'
    c += '<li>Seleccionar el <strong>responsable de salida</strong>.</li>\n'
    c += '<li>Hacer clic en <strong>Guardar pesaje</strong>.</li>\n'
    c += '</ol>\n</div>\n'
    c += '<div class="captura">\n' + img_html('balanza_pesaje_salida.png') + '\n<p>Figura 5: Pesaje de salida</p>\n</div>\n'
    return c


def contenido_iq():
    c = '<h1>3. Inspeccion Quimica</h1>\n'
    c += '<p>El modulo de <strong>Inspeccion Quimica</strong> (IQ) controla que la materia prima que ingresa cumpla con los requisitos de calidad y seguridad. Se verifica el certificado, los requisitos y la autorizacion de descarga.</p>\n'
    c += '<h2>3.1 Inicio de Inspeccion Quimica</h2>\n'
    c += '<p>Pantalla principal del modulo con acceso a las funciones de inspeccion.</p>\n'
    c += '<div class="captura">\n' + img_html('iq_inicio.png') + '\n<p>Figura 1: Inicio de Inspeccion Quimica</p>\n</div>\n'
    c += '<h2>3.2 Ingresos Pendientes de Inspeccion</h2>\n'
    c += '<p>Muestra los camiones que han pasado por balanza y estan listos para la inspeccion quimica.</p>\n'
    c += '<div class="captura">\n' + img_html('iq_pendientes.png') + '\n<p>Figura 2: Ingresos pendientes de inspeccion</p>\n</div>\n'
    c += '<h2>3.3 Control de Inspeccion</h2>\n'
    c += '<p>Al seleccionar un camion pendiente, se carga el formulario de control de inspeccion:</p>\n'
    c += '<div class="pasos">\n<ol>\n'
    c += '<li>Indicar si el <strong>ingresa con certificado</strong> (Si/No).</li>\n'
    c += '<li>Indicar si <strong>cumple requisitos</strong> (Si/No).</li>\n'
    c += '<li>Indicar si esta <strong>autorizado a descargar</strong> (Si/No).</li>\n'
    c += '<li>Completar las <strong>observaciones</strong> si corresponde.</li>\n'
    c += '<li>Seleccionar el <strong>responsable</strong> de la inspeccion.</li>\n'
    c += '<li>Hacer clic en <strong>Guardar</strong>.</li>\n'
    c += '</ol>\n</div>\n'
    c += '<div class="captura">\n' + img_html('iq_control.png') + '\n<p>Figura 3: Control de Inspeccion Quimica</p>\n</div>\n'
    c += '<h2>3.4 Controles de Dias No Laborables</h2>\n'
    c += '<p>Cuando un camion ingresa en un dia no laborable (feriado o fin de semana), la inspeccion se registra como pendiente y se controla posteriormente. Esta pantalla muestra esos controles pendientes.</p>\n'
    c += '<div class="captura">\n' + img_html('iq_controles_no_laborables.png') + '\n<p>Figura 4: Controles de dias no laborables</p>\n</div>\n'
    c += '<h2>3.5 Control de Inspeccion Pendiente</h2>\n'
    c += '<p>Al seleccionar un control pendiente, se completa el formulario de inspeccion que quedo pendiente por dia no laborable.</p>\n'
    c += '<div class="captura">\n' + img_html('iq_control_pendiente.png') + '\n<p>Figura 5: Control de inspeccion pendiente</p>\n</div>\n'
    return c


def contenido_pamo():
    c = '<h1>4. PAMO</h1>\n'
    c += '<p>El modulo de <strong>PAMO</strong> (Planta de Amoniaco) controla la presion y temperatura de los camiones que transportan <strong>Amoniaco</strong> o <strong>Hipoclorito</strong> durante la descarga.</p>\n'
    c += '<h2>4.1 Pendientes de Control</h2>\n'
    c += '<p>Muestra los camiones que han pasado por Inspeccion Quimica y estan listos para el control de presion y temperatura en PAMO.</p>\n'
    c += '<div class="captura">\n' + img_html('pamo_pendientes.png') + '\n<p>Figura 1: Pendientes de control PAMO</p>\n</div>\n'
    c += '<h2>4.2 Control de Presion y Temperatura</h2>\n'
    c += '<p>Al seleccionar un camion pendiente, se carga el formulario de control:</p>\n'
    c += '<div class="pasos">\n<ol>\n'
    c += '<li>Registrar la <strong>hora de ingreso</strong>.</li>\n'
    c += '<li>Ingresar la <strong>presion de ingreso</strong> (Kg/cm2).</li>\n'
    c += '<li>Ingresar la <strong>temperatura de ingreso</strong> (C).</li>\n'
    c += '<li>Registrar la <strong>hora de salida</strong>.</li>\n'
    c += '<li>Ingresar la <strong>presion de salida</strong> (Kg/cm2).</li>\n'
    c += '<li>Ingresar la <strong>temperatura de salida</strong> (C).</li>\n'
    c += '<li>Seleccionar el <strong>responsable</strong> del control.</li>\n'
    c += '<li>Hacer clic en <strong>Guardar</strong>.</li>\n'
    c += '</ol>\n</div>\n'
    c += '<div class="captura">\n' + img_html('pamo_control.png') + '\n<p>Figura 2: Control de presion y temperatura PAMO</p>\n</div>\n'
    return c


def contenido_psul():
    c = '<h1>5. PSUL</h1>\n'
    c += '<p>El modulo de <strong>PSUL</strong> (Planta de Azufre) controla la presion y temperatura de los camiones que transportan <strong>Azufre Liquido</strong> o <strong>Azufre Solido</strong> durante la descarga.</p>\n'
    c += '<h2>5.1 Pendientes de Control</h2>\n'
    c += '<p>Muestra los camiones que han pasado por Inspeccion Quimica y estan listos para el control de presion y temperatura en PSUL.</p>\n'
    c += '<div class="captura">\n' + img_html('psul_pendientes.png') + '\n<p>Figura 1: Pendientes de control PSUL</p>\n</div>\n'
    c += '<h2>5.2 Control de Presion y Temperatura</h2>\n'
    c += '<p>Al seleccionar un camion pendiente, se carga el formulario de control:</p>\n'
    c += '<div class="pasos">\n<ol>\n'
    c += '<li>Registrar la <strong>hora de ingreso</strong>.</li>\n'
    c += '<li>Ingresar la <strong>presion de ingreso</strong> (Kg/cm2).</li>\n'
    c += '<li>Ingresar la <strong>temperatura de ingreso</strong> (C).</li>\n'
    c += '<li>Registrar la <strong>hora de salida</strong>.</li>\n'
    c += '<li>Ingresar la <strong>presion de salida</strong> (Kg/cm2).</li>\n'
    c += '<li>Ingresar la <strong>temperatura de salida</strong> (C).</li>\n'
    c += '<li>Seleccionar el <strong>responsable</strong> del control.</li>\n'
    c += '<li>Hacer clic en <strong>Guardar</strong>.</li>\n'
    c += '</ol>\n</div>\n'
    c += '<div class="captura">\n' + img_html('psul_control.png') + '\n<p>Figura 2: Control de presion y temperatura PSUL</p>\n</div>\n'
    return c


def contenido_calidad():
    c = '<h1>6. Calidad</h1>\n'
    c += '<p>El modulo de <strong>Calidad</strong> gestiona los registros de calidad de los procedimientos y normativas vigentes. Permite visualizar los ultimos registros y agregar nuevos.</p>\n'
    c += '<h2>6.1 Gestion de Calidad</h2>\n'
    c += '<p>Esta pantalla muestra los ultimos 5 registros de calidad ordenados por fecha de vigencia y permite agregar nuevos registros.</p>\n'
    c += '<div class="pasos">\n<ol>\n'
    c += '<li>Ingresar la <strong>fecha de vigencia</strong> del registro.</li>\n'
    c += '<li>Ingresar la <strong>version</strong> del documento.</li>\n'
    c += '<li>Ingresar el <strong>numero de registro</strong> (ej: IN 11-IQ-07).</li>\n'
    c += '<li>Hacer clic en <strong>Agregar nuevo registro</strong>.</li>\n'
    c += '</ol>\n</div>\n'
    c += '<div class="captura">\n' + img_html('calidad_gestion.png') + '\n<p>Figura 1: Gestion de Calidad</p>\n</div>\n'
    return c


def contenido_shyma():
    c = '<h1>7. SHYMA</h1>\n'
    c += '<p>El modulo de <strong>SHYMA</strong> (Seguridad, Higiene y Medio Ambiente) controla los vehiculos en transito y puede rechazar una Hoja de Ruta (HDR) si detecta irregularidades en la carga o documentacion.</p>\n'
    c += '<h2>7.1 Vehiculos en Transito</h2>\n'
    c += '<p>Muestra todos los camiones que se encuentran en transito dentro de la planta con su HDR en estado Activo.</p>\n'
    c += '<div class="captura">\n' + img_html('shyma_en_transito.png') + '\n<p>Figura 1: Vehiculos en transito</p>\n</div>\n'
    c += '<h2>7.2 Rechazo de HDR</h2>\n'
    c += '<p>Al seleccionar un vehiculo en transito, se muestra el formulario de rechazo con los datos del ingreso (solo lectura) y los campos para registrar el rechazo:</p>\n'
    c += '<div class="advertencia">\n<strong>Advertencia:</strong> Esta a punto de rechazar una HDR. No se podra deshacer el rechazo.\n</div>\n'
    c += '<div class="pasos">\n<ol>\n'
    c += '<li>Seleccionar el <strong>responsable de SHYMA</strong> que realiza el rechazo.</li>\n'
    c += '<li>Completar la <strong>observacion</strong> con el motivo del rechazo.</li>\n'
    c += '<li>Hacer clic en <strong>Guardar</strong>.</li>\n'
    c += '</ol>\n</div>\n'
    c += '<div class="captura">\n' + img_html('shyma_rechazo.png') + '\n<p>Figura 2: Rechazo de HDR</p>\n</div>\n'
    return c


def contenido_introduccion():
    c = '<h1>Introduccion</h1>\n'
    c += '<p>El <strong>Sistema de Ingreso de Materia Prima</strong> es una aplicacion web desarrollada para gestionar el circuito completo de ingreso de camiones con materia prima a la planta. El sistema permite registrar, controlar y dar seguimiento a cada vehiculo desde su ingreso por Porteria 2 hasta su egreso, pasando por balanza, inspeccion quimica y controles de presion/temperatura.</p>\n'
    c += '<h2>Flujo General del Circuito</h2>\n'
    c += '<p>El circuito completo de un camion es el siguiente:</p>\n'
    c += '<div class="pasos">\n<ol>\n'
    c += '<li><strong>Porteria 2</strong>: Registro del ingreso del camion y control de EPP.</li>\n'
    c += '<li><strong>Balanza</strong>: Pesaje de entrada del camion con la materia prima.</li>\n'
    c += '<li><strong>Inspeccion Quimica</strong>: Control de certificado, requisitos y autorizacion de descarga.</li>\n'
    c += '<li><strong>PAMO/PSUL</strong>: Control de presion y temperatura durante la descarga (segun producto).</li>\n'
    c += '<li><strong>Almacen PQ</strong>: Descarga de la materia prima.</li>\n'
    c += '<li><strong>Balanza</strong>: Pesaje de salida del camion vacio.</li>\n'
    c += '<li><strong>Porteria 2</strong>: Verificacion y egreso del camion.</li>\n'
    c += '</ol>\n</div>\n'
    c += '<h2>Productos y su Circuito</h2>\n'
    c += '<table class="tabla-info">\n<tr><th>Producto</th><th>Control de Presion/Temperatura</th></tr>\n'
    c += '<tr><td>Amoniaco</td><td>PAMO</td></tr>\n'
    c += '<tr><td>Hipoclorito</td><td>PAMO</td></tr>\n'
    c += '<tr><td>Azufre Liquido</td><td>PSUL</td></tr>\n'
    c += '<tr><td>Azufre Solido</td><td>PSUL</td></tr>\n'
    c += '</table>\n'
    c += '<h2>Estados de la HDR</h2>\n'
    c += '<table class="tabla-info">\n<tr><th>Estado</th><th>Descripcion</th></tr>\n'
    c += '<tr><td>Activo</td><td>La HDR esta en curso, el camion se encuentra en transito.</td></tr>\n'
    c += '<tr><td>Anulado</td><td>La HDR fue anulada.</td></tr>\n'
    c += '<tr><td>Finalizado</td><td>El circuito se completo y el camion egreso de la planta.</td></tr>\n'
    c += '<tr><td>RechazoConfirmado</td><td>La HDR fue rechazada por SHYMA y esta pendiente de egreso.</td></tr>\n'
    c += '<tr><td>Rechazado</td><td>La HDR fue rechazada y el camion egreso.</td></tr>\n'
    c += '</table>\n'
    c += '<h2>Sectores del Sistema</h2>\n'
    c += '<table class="tabla-info">\n<tr><th>Sector</th><th>Funcion</th></tr>\n'
    c += '<tr><td>Porteria 2</td><td>Registro de ingreso y egreso de camiones, control de EPP.</td></tr>\n'
    c += '<tr><td>Almacen PQ</td><td>Pesaje de entrada en balanza.</td></tr>\n'
    c += '<tr><td>Inspeccion PQ</td><td>Control de calidad de la materia prima.</td></tr>\n'
    c += '<tr><td>PAMO</td><td>Control de presion y temperatura de Amoniaco e Hipoclorito.</td></tr>\n'
    c += '<tr><td>PSUL</td><td>Control de presion y temperatura de Azufre.</td></tr>\n'
    c += '<tr><td>Almacen PQ E</td><td>Pesaje de salida en balanza.</td></tr>\n'
    c += '<tr><td>SHYMA</td><td>Control de vehiculos en transito y rechazo de HDR.</td></tr>\n'
    c += '</table>\n'
    return c


# ============================================================
# GENERACION DE PDFs
# ============================================================

def main():
    print('=== Generando manuales ===')

    sectores = [
        ('Manual de Porteria 2', contenido_porteria(), 'Manual_Porteria2.pdf'),
        ('Manual de Balanza', contenido_balanza(), 'Manual_Balanza.pdf'),
        ('Manual de Inspeccion Quimica', contenido_iq(), 'Manual_InspeccionQuimica.pdf'),
        ('Manual de PAMO', contenido_pamo(), 'Manual_PAMO.pdf'),
        ('Manual de PSUL', contenido_psul(), 'Manual_PSUL.pdf'),
        ('Manual de Calidad', contenido_calidad(), 'Manual_Calidad.pdf'),
        ('Manual de SHYMA', contenido_shyma(), 'Manual_SHYMA.pdf'),
    ]

    for titulo, contenido, archivo in sectores:
        print('Generando: ' + archivo)
        html = generar_html_sector(titulo, contenido)
        # Generar PDF
        generar_pdf(html, archivo)
        # Guardar HTML editable
        html_archivo = archivo.replace('.pdf', '.html')
        guardar_html(html, html_archivo)

    # Manual completo unificado
    print('Generando: Manual_Usuario_Completo.pdf')
    contenido_completo = contenido_introduccion()
    contenido_completo += contenido_porteria()
    contenido_completo += contenido_balanza()
    contenido_completo += contenido_iq()
    contenido_completo += contenido_pamo()
    contenido_completo += contenido_psul()
    contenido_completo += contenido_calidad()
    contenido_completo += contenido_shyma()
    html_completo = generar_html_sector('Manual de Usuario Completo', contenido_completo)
    generar_pdf(html_completo, 'Manual_Usuario_Completo.pdf')
    guardar_html(html_completo, 'Manual_Usuario_Completo.html')

    print('=== MANUALES GENERADOS ===')


if __name__ == '__main__':
    main()