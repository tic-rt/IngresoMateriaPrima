import os
from playwright.sync_api import sync_playwright

OUTPUT_DIR = 'manuales'
HTML_DIR = 'manuales_html'


def convertir_html_a_pdf(html_archivo, pdf_archivo):
    """Convierte un archivo HTML a PDF usando Playwright (Chromium)"""
    ruta_html = os.path.join(HTML_DIR, html_archivo)
    ruta_pdf = os.path.join(OUTPUT_DIR, pdf_archivo)

    if not os.path.exists(ruta_html):
        print(f'  ERROR: No se encuentra el archivo {ruta_html}')
        return False

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f'file://{os.path.abspath(ruta_html)}', wait_until='networkidle')
        page.pdf(path=ruta_pdf, format='A4', print_background=True,
                 margin={'top': '20mm', 'bottom': '20mm', 'left': '15mm', 'right': '15mm'})
        browser.close()
    print(f'  PDF generado: {ruta_pdf}')
    return True


def main():
    print('=== Convirtiendo HTMLs editados a PDF ===')

    # Mapeo de archivos HTML a archivos PDF
    archivos = [
        ('Manual_Porteria2.html', 'Manual_Porteria2.pdf'),
        ('Manual_Balanza.html', 'Manual_Balanza.pdf'),
        ('Manual_InspeccionQuimica.html', 'Manual_InspeccionQuimica.pdf'),
        ('Manual_PAMO.html', 'Manual_PAMO.pdf'),
        ('Manual_PSUL.html', 'Manual_PSUL.pdf'),
        ('Manual_Calidad.html', 'Manual_Calidad.pdf'),
        ('Manual_SHYMA.html', 'Manual_SHYMA.pdf'),
        ('Manual_Usuario_Completo.html', 'Manual_Usuario_Completo.pdf'),
    ]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for html_archivo, pdf_archivo in archivos:
        print(f'Procesando: {html_archivo}')
        convertir_html_a_pdf(html_archivo, pdf_archivo)

    print('=== CONVERSION COMPLETADA ===')


if __name__ == '__main__':
    main()