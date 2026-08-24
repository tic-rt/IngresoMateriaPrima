# Herramientas de desarrollo

Carpeta con utilidades para generar y mantener los manuales de usuario del sistema. No forman parte del runtime de Django: son scripts sueltos de desarrollo.

| Script | Finalidad |
|---|---|
| `capturar_pantallas.py` | Automatiza con Playwright el login por sector y captura las pantallas principales del sistema en PNG en `capturas/`. Usa `ids_captura.json` para armar URLs con registros reales. |
| `convertir_html_a_pdf.py` | Convierte los manuales editables (`manuales_html/*.html`) a PDF A4 (`manuales/`) vía Chromium. |
| `generar_manual.py` | Genera los manuales por sector y el manual completo: arma el HTML (CSS A4 + capturas base64 de `capturas/`) y produce `manuales/*.pdf` **y** `manuales_html/*.html`. |
| `seed_manual.py` | Crea/obtiene datos de ejemplo (HDRs, ingresos con EPP, balanzas, inspecciones, controles PAMO/PSUL, egresos, calidad) para que las capturas muestren pantallas con info real. |
| `ids_captura.json` | Config auxiliar de IDs por flujo (`control_epp`, `pesaje_entrada`, `inspeccion`, `pamo`, `psul`, `pesaje_salida`, `egreso`, `shyma`) usada por `capturar_pantallas.py`. |

## Flujo típico

```bash
python seed_manual.py            # 1. datos de ejemplo
python capturar_pantallas.py     # 2. capturas PNG
python generar_manual.py         # 3. genera HTML + PDF + HTML editable
python convertir_html_a_pdf.py   # 4. (opcional) regenerar PDFs desde HTML editado
```

## `ids_captura.json`

Config auxiliar con los IDs reales de los registros sembrados (`id_ingreso`, `id_hdr`) por flujo (`control_epp`, `pesaje_entrada`, `inspeccion`, `pamo`, `psul`, `pesaje_salida`, `egreso`, `shyma`) que usa `capturar_pantallas.py` para armar las URLs de los formularios con detalle.

---
*Documentación generada desde el código real de las cuatro herramientas y su JSON.*