import os
import json
import time
from playwright.sync_api import sync_playwright

BASE_URL = 'http://127.0.0.1:8000'
OUTPUT_DIR = 'capturas'

# Cargar IDs de ingresos
with open('ids_captura.json', 'r') as f:
    IDS = json.load(f)

# Usuarios por sector
USUARIOS = {
    'porteria': {'username': 'Porteria2', 'password': 'Password2024'},
    'balanza': {'username': 'Balanza', 'password': 'B4l4nz4$2024'},
    'laboratorio': {'username': 'Laboratorio', 'password': 'L4b0r4t0r10$'},
    'pamo': {'username': 'Pamo', 'password': 'Pamo#2025'},
    'psul': {'username': 'Psul', 'password': '2025%Psul'},
    'shyma': {'username': 'Shyma', 'password': 'Shyma2024$'},
    'admin': {'username': 'Tic', 'password': 'Magenta1'},
}


def login(page, username, password):
    """Inicia sesion en el sistema"""
    page.goto(f'{BASE_URL}/auth/login/')
    page.wait_for_load_state('networkidle')
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    page.wait_for_load_state('networkidle')
    time.sleep(1)


def capturar(page, url, nombre, espera=1.5):
    """Navega a una URL y captura la pantalla"""
    page.goto(url)
    page.wait_for_load_state('networkidle')
    time.sleep(espera)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    page.screenshot(path=f'{OUTPUT_DIR}/{nombre}.png', full_page=True)
    print(f'  Capturada: {nombre}.png')


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1366, 'height': 768})
        page = context.new_page()

        # ============================================================
        # PORTERIA 2
        # ============================================================
        print('=== Capturando Porteria 2 ===')
        login(page, USUARIOS['porteria']['username'], USUARIOS['porteria']['password'])

        # Dashboard Porteria
        capturar(page, f'{BASE_URL}/porteria/', 'porteria_dashboard')

        # Nuevo Ingreso
        capturar(page, f'{BASE_URL}/porteria/nuevoIngreso', 'porteria_nuevo_ingreso')

        # Controles EPP pendientes
        capturar(page, f'{BASE_URL}/porteria/controlEppPendientes', 'porteria_controles_epp_pendientes')

        # Control EPP (formulario)
        if 'control_epp' in IDS:
            ids = IDS['control_epp']
            capturar(page, f"{BASE_URL}/porteria/controlEpp/?id_hdr={ids['id_hdr']}&id_ingreso={ids['id_ingreso']}", 'porteria_control_epp')

        # Egresos pendientes
        capturar(page, f'{BASE_URL}/porteria/egresosPendientes', 'porteria_egresos_pendientes')

        # Egreso (formulario)
        if 'egreso' in IDS:
            ids = IDS['egreso']
            capturar(page, f"{BASE_URL}/porteria/egreso/?id_ingreso={ids['id_ingreso']}", 'porteria_egreso')

        # ============================================================
        # BALANZA
        # ============================================================
        print('=== Capturando Balanza ===')
        login(page, USUARIOS['balanza']['username'], USUARIOS['balanza']['password'])

        # Inicio Balanza
        capturar(page, f'{BASE_URL}/balanza/inicio/', 'balanza_inicio')

        # Pendientes de pesaje entrada
        capturar(page, f'{BASE_URL}/balanza/pendientes', 'balanza_pendientes')

        # Pesaje entrada (formulario)
        if 'pesaje_entrada' in IDS:
            ids = IDS['pesaje_entrada']
            capturar(page, f"{BASE_URL}/balanza/pesaje/?id_ingreso={ids['id_ingreso']}", 'balanza_pesaje_entrada')

        # Egresos (pesaje salida)
        capturar(page, f'{BASE_URL}/balanza/egresos', 'balanza_egresos')

        # Pesaje salida (formulario)
        if 'pesaje_salida' in IDS:
            ids = IDS['pesaje_salida']
            capturar(page, f"{BASE_URL}/balanza/pesajeSalida/?id_ingreso={ids['id_ingreso']}", 'balanza_pesaje_salida')

        # ============================================================
        # INSPECCION QUIMICA
        # ============================================================
        print('=== Capturando Inspeccion Quimica ===')
        login(page, USUARIOS['laboratorio']['username'], USUARIOS['laboratorio']['password'])

        # Inicio Laboratorio
        capturar(page, f'{BASE_URL}/inspeccionPQ/', 'iq_inicio')

        # Pendientes de inspeccion
        capturar(page, f'{BASE_URL}/inspeccionPQ/pendientes', 'iq_pendientes')

        # Control de inspeccion (formulario)
        if 'inspeccion' in IDS:
            ids = IDS['inspeccion']
            capturar(page, f"{BASE_URL}/inspeccionPQ/inspeccion/?id_ingreso={ids['id_ingreso']}&id_hdr={ids['id_hdr']}", 'iq_control')

        # Controles dias no laborables
        capturar(page, f'{BASE_URL}/inspeccionPQ/inspeccion_pendiente/', 'iq_controles_no_laborables')

        # Control inspeccion pendiente (formulario)
        if 'inspeccion_pendiente' in IDS:
            ids = IDS['inspeccion_pendiente']
            capturar(page, f"{BASE_URL}/inspeccionPQ/control_inspeccion/?id_ingreso={ids['id_ingreso']}&id_hdr={ids['id_hdr']}", 'iq_control_pendiente')

        # ============================================================
        # PAMO
        # ============================================================
        print('=== Capturando PAMO ===')
        login(page, USUARIOS['pamo']['username'], USUARIOS['pamo']['password'])

        # Pendientes PAMO
        capturar(page, f'{BASE_URL}/PAMO/pendientes', 'pamo_pendientes')

        # Control PAMO (formulario)
        if 'pamo' in IDS:
            ids = IDS['pamo']
            capturar(page, f"{BASE_URL}/PAMO/control/?id_ingreso={ids['id_ingreso']}", 'pamo_control')

        # ============================================================
        # PSUL
        # ============================================================
        print('=== Capturando PSUL ===')
        login(page, USUARIOS['psul']['username'], USUARIOS['psul']['password'])

        # Pendientes PSUL
        capturar(page, f'{BASE_URL}/PSUL/pendientes', 'psul_pendientes')

        # Control PSUL (formulario)
        if 'psul' in IDS:
            ids = IDS['psul']
            capturar(page, f"{BASE_URL}/PSUL/control/?id_ingreso={ids['id_ingreso']}", 'psul_control')

        # ============================================================
        # CALIDAD
        # ============================================================
        print('=== Capturando Calidad ===')
        login(page, USUARIOS['admin']['username'], USUARIOS['admin']['password'])

        # Gestion de calidad
        capturar(page, f'{BASE_URL}/calidad/gestion/', 'calidad_gestion')

        # ============================================================
        # SHYMA
        # ============================================================
        print('=== Capturando SHYMA ===')
        login(page, USUARIOS['shyma']['username'], USUARIOS['shyma']['password'])

        # Vehiculos en transito
        capturar(page, f'{BASE_URL}/shyma/en_transito/', 'shyma_en_transito')

        # Rechazo de HDR (formulario)
        if 'shyma' in IDS:
            ids = IDS['shyma']
            capturar(page, f"{BASE_URL}/shyma/ingreso/?id_ingreso={ids['id_ingreso']}&id_hdr={ids['id_hdr']}", 'shyma_rechazo')

        browser.close()
        print('=== CAPTURAS COMPLETADAS ===')


if __name__ == '__main__':
    main()