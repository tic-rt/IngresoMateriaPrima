# Corrections.md — Hallazgos y recomendaciones

**Proyecto:** IngresoMateriaPrima · **Fecha:** 2026-08-24 · **Alcance:** auditoría de código fuente (models, views, urls, templates, settings, scripts auxiliares).

Checklist de trabajo: marcar `[x]` cada ítem al corregirlo.

## Resumen priorizado

| ID | Hallazgo | Ubicación | Esfuerzo | Impacto | Estado |
|---|---|---|---|---|---|
| C-01 | Vistas sin autenticación/permisos | `calidad`, `laboratorio`, `app` | Minutos | Alto | ☐ |
| C-02 | Bug de plantilla: sección HDR visible para todos | `base.html` | 1 línea | Alto | ☐ |
| C-03 | Credenciales en texto plano en el repo | `resetdb.py`, `capturar_pantallas.py` | Bajo | Alto | [x] |
| C-04 | Settings de producción por verificar | `settings.py` | Bajo | Alto | ☐ |
| C-05 | Strings mágicos de `sector`/`estado` | varias vistas | Medio | Alto | ☐ |
| C-06 | `try/except Exception` amplios + `print()` | todas las apps | Bajo | Medio | ☐ |
| C-07 | `class meta` en minúscula (Meta ignorada) | `personal/models.py` | 1 línea | Medio | ☐ |
| C-08 | Inconsistencias de modelos | `calidad`, `pamo`, `balanza` | Bajo/Medio | Medio | ☐ |
| C-09 | Duplicación pamo/psul | `pamo/`, `psul/` | Medio | Medio | ☐ |
| C-10 | Sin tests | todos los `tests.py` | Medio | Medio-Alto | ☐ |
| C-11 | `USE_TZ = False` | `settings.py` | Medio | Medio | ☐ |
| C-12 | SQLite y concurrencia de escritura | `settings.py` | Medio | Según uso | ☐ |
| C-13 | Scripts JS en `<head>` sin `defer` | `base.html` | Bajo | Bajo | ☐ |
| C-14 | `.gitignore` y README mínimos | raíz | Bajo | Bajo | ☐ |

---

## 🔴 Prioridad alta — Seguridad

### C-01 — Vistas sin autenticación ni permisos

**a)** `calidad/views.py → agregar_calidad`: única vista pública de escritura del sistema. Cualquier visitante anónimo puede insertar registros de calidad vía POST directo.

```python
# Actual
def agregar_calidad(request):
    ...
# Propuesto
@login_required
@permission_required('calidad.add_calidad', login_url='index')
def agregar_calidad(request):
    ...
```

**b)** `laboratorio/views.py → pendientes_control`: renderiza el listado de ingresos de días no laborables sin decoradores (las demás vistas de la app sí los tienen).

```python
@login_required
@permission_required('porteria2.view_ingreso', raise_exception=True)
def pendientes_control(request):
```

**c)** `app/views.py → cantidad_camiones` y `transito`: endpoints JSON sin `@login_required`; exponen conteos operativos. Agregar `@login_required` (el front que los consume ya está tras login).

### C-02 — Sección HDR visible para todos (`base.html`)

En la barra lateral:

```html
{% if 'user.is_autenticated' or user.is_superuser %}
```

Es un **string literal siempre verdadero** (además del typo `is_autenticated`): la sección **HDR aparece para cualquier usuario**, sin importar su grupo.

```html
{# Propuesto #}
{% if 'hdr.view_hdr' in perms or user.is_superuser %}
```

(`perms` está disponible en plantillas sin configurar nada.)

### C-03 — Credenciales en texto plano en el repositorio

`resetdb.py` (`USUARIOS = [{'username': 'Tic', 'password': 'Magenta1'}, …]`) y `app/Tools/capturar_pantallas.py` (`USUARIOS` con las mismas contraseñas) versionan credenciales reales de demo.

- Mover usuario/contraseña a variables de entorno o `.env` (fuera del repo).
- Alternativa mínima si son solo datos demo: dejar usuarios demo sin permisos reales y documentarlo; nunca reutilizar esas claves en producción.

### C-04 — Settings de producción por verificar

No se auditó el bloque superior de `settings.py`. Antes de un despliegue real confirmar:

- `SECRET_KEY` desde variable de entorno (no hardcodeada).
- `DEBUG = False` y `ALLOWED_HOSTS` explícito.
- Servir estáticos con `collectstatic` + whitenoise/nginx (hoy dependen del runserver).