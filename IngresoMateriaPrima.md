# IngresoMateriaPrima — Documentación técnica

Documento generado a partir de la lectura del código fuente (models, views, urls, forms, dashboards, templates, settings y scripts auxiliares).

## 1. Funcionalidad general

Aplicación web Django que gestiona el **ingreso de camiones con materia prima** a la planta: registro en portería, control de Elementos de Protección Personal (EPP), pesaje en balanza, inspección química, controles de presión/temperatura (PAMO/PSUL), monitoreo de vehículos en tránsito por SHYMA y egresos.

El eje del sistema es la **HDR (Hoja de Ruta)**: cada camión genera una HDR al ingresar y ésta cambia de `sector` y `estado` a medida que avanza por las etapas del circuito hasta su egreso.

Productos que maneja: **Amoníaco, Hipoclorito, Azufre Líquido y Azufre Sólido, Otros**.

## 2. Stack tecnológico

| Tecnología | Uso |
|---------------------------------------------|-----------------------------------------------------------|
| Django 5.1 (Python) + SQLite (`db.sqlite3`) | Framework web (patrón MTV)                                |
| Bootstrap 5.3.2 + Bootstrap Icons           | UI responsive; offcanvas para menú lateral en móvil       |
| Chart.js                                    | Gráficos de dashboards                                    |
| DataTables                                  | Tablas con búsqueda/filtrado client-side                  |
| SweetAlert2 + django-sweetify               | Mensajes de éxito/error/advertencia                       |
| django-simple-history                       | Auditoría histórica de modelos de negocio                 |
| django-crispy-forms (bootstrap5)            | Render de formularios                                     |
| xhtml2pdf + reportlab + pypdf               | Exportación de HDR a PDF (con sello diagonal "RECHAZADO") |
| Playwright (Chromium)                       | Solo herramientas de manuales (`app/Tools/`)              |

## 3. Arquitectura y estructura

Proyecto Django multi-app: **una app por dominio de negocio**, más la app `app` con home, endpoints JSON, plantillas base y estáticos.

```
IngresoMateriaPrima/
├── IngresoMateriaPrima/     # settings.py y urls.py del proyecto
├── app/                     # Home, JSONs, base.html, css/img/vendor, context processor
│   └── Tools/               # Scripts de generación de manuales (ver app/Tools/Tools.md)
├── base/                    # Modelo abstracto Base (soft delete + auditoría)
├── auth/                    # login / logout
├── hdr/                     # Hoja de Ruta: listado paginado y exportación PDF
├── personal/                # Responsables por sector
├── transporte/              # Empresas, camiones, semis, conductores
├── proveedores/             # Proveedores, productos y relación N-N
├── porteria2/               # Ingresos, control de EPP y egresos (+ dashboard)
├── balanza/                 # Pesajes de entrada/salida (+ dashboard de kilos)
├── laboratorio/             # Inspección química (+ días no laborables, dashboard)
├── pamo/  ·  psul/          # Controles de presión y temperatura
├── calidad/                 # Registros de calidad
├── shyma/                   # Tránsito y rechazo de HDRs
├── manuales_html/           # Manuales HTML (servidos como estáticos)
├── manuales/                # PDFs de manuales
├── capturas/                # Capturas usadas en los manuales
└── documentacion/           # Diagramas (clases.uxf)
```

Cada app sigue la convención estándar de Django (`models.py`, `views.py`, `forms.py`, `urls.py` y opcionalmente `dashboard.py` para endpoints JSON de gráficos). Las rutas se montan en `IngresoMateriaPrima/urls.py` con prefijos: `/porteria/`, `/balanza/`, `/inspeccionPQ/`, `/PAMO/`, `/PSUL/`, `/hdr/`, `/calidad/`, `/shyma/`, `/transportes/`, `/personal/`, `/proveedor-producto/`, `/auth/` y la raíz `/` para `app`.

## 4. Modelo de datos

`base.models.Base` es un modelo abstracto del que heredan los modelos de negocio:
- `id`, fechas de creación/modificación/eliminación.
- **Soft delete**: `delete()` marca `is_deleted=True`; `restore()` lo revierte. Las vistas filtran siempre por `is_deleted=False`.
- Auditoría con `HistoricalRecords` (django-simple-history).

| App           | Modelo                                       | Descripción                                                      | Relación con HDR                                            |
|---------------|----------------------------------------------|------------------------------------------------------------------|----------------------------------|
| hdr           | `HDR`                                        | Hoja de Ruta: `sector`, `estado`, `observacion`, `rechazado_por` | — (es el eje)                    |
| personal      | `Personal`                                   | Responsable por sector (legajo único; soft delete propio)        | FK en todas las etapas           |
| transporte    | `Transporte`, `Camion`, `Semi`, `Conductor`  | Maestros de flota con vencimientos (seguro/carnet)               | FK desde Ingreso                 |
| proveedores   | `Proveedor`, `Producto`, `ProveedorProducto` | Maestros y relación N-N proveedor-producto                       | FK desde Ingreso/Balanza         |
| porteria2     | `Ingreso`                                    | Ingreso del camión: remito (único), producto, conductor, patentes|                                  |
|               |                                              | `ingresado`, `laborable`, ingreso para calefacción               | OneToOne                         |
| porteria2     | `EPP`                                        | Control de EPP                                                   | OneToOne                         |
| porteria2     | `Egreso`                                     | Verificación de vehículo/carga y autorización de salida          | OneToOne                         |
| balanza       | `Balanza`                                    | Pesajes: origen/FMRT/vacío/taquilla/bolsa-tarima/neto,           |                                  |
|               |                                              | responsables entrada/salida                                      | OneToOne                         |
| laboratorio   | `Inspeccion`                                 | Certificado, cumple requisitos, autorizado a descargar, `cerrado`| OneToOne                         |
| pamo          | `PamoPsul`                                   | Presión/temperatura de ingreso y salida                          |                                  |
|               |                                              | (modelo compartido por PAMO y PSUL)                              | ForeignKey                       |
| calidad       | `Calidad`                                    | Versión + registro + fecha de vigencia (no hereda Base)          | —                                |

## 5. Flujo operativo (ciclo de vida de la HDR)

```
Portería 2 ──► Balanza (Almacén PQ) ──► Inspección PQ ──► PAMO | PSUL ──► Almacén PQ E ──► Portería 2 E
  ingreso/EPP      pesaje entrada        inspección      presión/temp       pesaje salida       egreso
```

1. **Nuevo ingreso** (`porteria/guardarNuevoIngreso`) — crea la `HDR` (sector `Porteria 2`, estado `Activo`) y el `Ingreso` (`ingresado=False`); redirige al control EPP.
2. **Control de EPP** (`controlEpp` / `guardarControlEpp`) — si cumple, `ingresado=True` y queda pendiente de balanza; si no, puede registrarse un rechazo (`guardarRechazo`).
3. **Pesaje de entrada** (`balanza/guardarPesaje`) — registra pesos y deriva la HDR: normalmente a `Inspeccion PQ`; según el producto puede ir directo a `PAMO`, `PSUL` o `Almacen PQ E`.
4. **Inspección Química** (`inspeccionPQ/guardar_inspeccion`) — certificado/requisitos/descarga; según resultado y producto deriva a `PAMO`, `PSUL` o `Almacen PQ E`. Para **días no laborables** existe el flujo alternativo `inspeccion_pendiente`: la inspección queda abierta (`cerrado=False`) y se completa después con `guardar_inspeccion_pendiente`.
5. **PAMO / PSUL** (`guardarPamo` / `guardarPsul`) — presión y temperatura de ingreso/salida; mueve la HDR a `Almacen PQ E`.
6. **SHYMA** (`en_transito` / `guardar_rechazo`) — monitorea camiones con HDR `Activo`; puede rechazarla: estado `RechazoConfirmado`, sector `Porteria 2 E`, guarda responsable del rechazo y observación acumulativa.
7. **Pesaje de salida** (`pesajeSalida` / `guardarPesaje2`) — completa los pesos netos del circuito.
8. **Egreso** (`egresosPendientes` / `guardarEgreso`) — verifica y autoriza la salida: estado `Finalizado`, o `Rechazado` si venía de un rechazo confirmado.

Estados posibles de la HDR: `Activo`, `Anulado`, `Finalizado`, `RechazoConfirmado`, `Rechazado`.

Todas las escrituras relevantes usan `@transaction.atomic` y validan existencia/estado de los IDs recibidos antes de guardar.

## 6. Seguridad y permisos

- Vistas protegidas con `@login_required` + `@permission_required('<app>.<accion>_<modelo>')` (con redirección a `index` o excepción 403).
- Grupos por sector creados por `resetdb.py`: `G_Porteria2`, `G_Balanza`, `G_Laboratorio`, `G_Pamo`, `G_Psul`, `G_Shyma`, cada uno con los permisos CRUD de sus modelos. La plantilla además contempla `G_Calidad` para la sección Calidad.
- Usuarios demo: `Tic` (superusuario), `Porteria2`, `Balanza`, `Laboratorio`, `Pamo`, `Psul`, `Shyma`.
- El context processor `grupos_usuario` (`app/context_processors.py`) expone los grupos del usuario a todas las plantillas: el menú lateral muestra solo las secciones permitidas y el enlace **Manual de uso** abre el manual HTML del sector (superusuario → `Manual_Usuario_Completo.html`).
- Login/logout en `/auth/login/` y `/auth/logout/`.

## 7. Vistas, dashboards y exportación

| Ruta                                                    | Descripción                                                                                                       |
|---------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| `/porteria/api/dashboard/?periodo=hoy\|semana\|mensual` | JSON del dashboard de portería: ingresos por empresa, en tránsito por producto y totales                          |
| `/balanza/api/dashboard-kilos/`                         | JSON de kilos/pesajes para el gráfico de balanza                                                                  |
| `/inspeccionPQ/…` (`dashboard_inspecciones`)            | Aceptados vs rechazados por producto o proveedor                                                                  |
| `/cantidad_camiones/`                                   | JSON: ingresos de hoy por producto                                                                                |
| `/transito/`                                            | JSON: ingresados / en tránsito / finalizados hoy                                                                  |
| `/hdr/lista/`                                           | Listado paginado (20 registros/página) de ingresos/HDR                                                            |
| `/hdr/exportar/?id_hdr=…`                               | PDF de la HDR completa; si fue rechazada superpone sello diagonal "RECHAZADO" (reportlab + pypdf sobre xhtml2pdf) |

Los dashboards consumen estos JSON con `fetch()` y renderizan gráficos Chart.js; las tablas usan DataTables.

## 8. Front-end

- Plantilla base `base.html`: header sticky con logo/título, navbar superior (Inicio, Portería, Balanza, Inspección Química) y **barra lateral** con secciones por grupo (Portería, Balanza, IQ con submenú Transportes, PAMO, PSUL, HDR, Calidad, SHYMA y Manual de uso).
- Responsive: en `<768px` la barra lateral es un offcanvas (`offcanvas-md`) que abre con hamburguesa y se cierra automáticamente al navegar.
- Formularios con crispy-forms (Bootstrap 5); avisos con SweetAlert2 vía `sweetify`.

## 9. Herramientas auxiliares (`app/Tools/`)

Fuera del runtime de Django; documentadas en `app/Tools/Tools.md`:

1. `seed_manual.py` — siembra datos demo (HDRs, ingresos con EPP, pesajes, inspecciones, PAMO/PSUL, egresos, calidad).
2. `capturar_pantallas.py` — Playwright: login por sector y capturas PNG a `capturas/` (usa `ids_captura.json`).
3. `generar_manual.py` — arma los manuales HTML (capturas embebidas en base64) en `manuales_html/` y PDF en `manuales/`.
4. `convertir_html_a_pdf.py` — regenera los PDF desde los HTML editados.

Además, `resetdb.py` (raíz) recrea la BD demo: elimina/migra, crea grupos, usuarios y maestros (personal, transporte, proveedores/productos).

## 10. Configuración relevante (`settings.py`)

- Base de datos SQLite local (`db.sqlite3`); `LANGUAGE_CODE='es-ES'`; `TIME_ZONE='America/Argentina/Buenos_Aires'`; `USE_TZ=False`.
- Estáticos: `STATIC_URL='static/'` y `STATICFILES_DIRS=[BASE_DIR / 'manuales_html']` → manuales accesibles en `/static/Manual_*.html`.
- `INSTALLED_APPS`: apps de dominio + `simple_history`, `crispy_forms`, `django.contrib.staticfiles`.
- Sweetify configurado sobre SweetAlert2; crispy con template pack `bootstrap5`.

## 11. Ejecución

```bash
python manage.py check
python resetdb.py            # BD demo + usuarios/grupos (opcional)
python manage.py runserver   # http://127.0.0.1:8000 → login en /auth/login/
```

---

*Documento generado por lectura del código fuente: models/views/urls/forms/dashboard de cada app, templates/base.html, settings.py, resetdb.py y app/Tools/.*