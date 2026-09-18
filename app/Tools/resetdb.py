import os
import sys
import json
import django
from datetime import date, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Raíz del proyecto: permite importar 'IngresoMateriaPrima.settings' desde cualquier cwd
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Carga explícita del .env para usar la conexión SQL configurada
load_dotenv(PROJECT_ROOT / 'IngresoMateriaPrima' / '.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IngresoMateriaPrima.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User, Group, Permission
from personal.models import Personal
from transporte.models import Transporte, Camion, Semi, Conductor
from proveedores.models import Proveedor, Producto, ProveedorProducto


GRUPOS = json.loads(os.environ.get('GRUPOS_JSON', '[]'))
USUARIOS = json.loads(os.environ.get('USUARIOS_JSON', '[]'))
if not GRUPOS or not USUARIOS:
    raise SystemExit('resetdb: faltan GRUPOS_JSON / USUARIOS_JSON en el .env.')


def eliminar_y_migrar():
    """Elimina los datos de la BD configurada (SQLite o SQL/MySQL) y ejecuta migrate."""
    from django.conf import settings
    from django.db import connection

    engine = settings.DATABASES['default']['ENGINE']
    connection.close()  # cerrar conexión antes de eliminar archivo/tablas

    if 'sqlite' in engine:
        db_path = settings.DATABASES['default']['NAME']
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f'Base de datos SQLite eliminada: {db_path}')
        else:
            print(f'No se encontró el archivo SQLite: {db_path}')
    else:
        # MySQL / otras SQL: vaciar el esquema eliminando todas las tablas de la BD actual
        with connection.cursor() as cursor:
            if 'mysql' in engine:
                cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
            tablas = connection.introspection.table_names()
            for tabla in tablas:
                sql = f'DROP TABLE IF EXISTS {connection.ops.quote_name(tabla)}'
                if 'postgresql' in engine:
                    sql += ' CASCADE'
                cursor.execute(sql)
            if 'mysql' in engine:
                cursor.execute('SET FOREIGN_KEY_CHECKS = 1')
            print(f'Base SQL vaciada: {len(tablas)} tabla(s) eliminada(s) en '
                  f'{settings.DATABASES["default"]["NAME"]}.')
    call_command('makemigrations', verbosity=1)
    call_command('migrate', verbosity=1)
    call_command('makemigrations', verbosity=1)
    print('Migraciones aplicadas.')


def recrear_usuarios_grupos():
    """Recrea los grupos y usuarios definidos en GRUPOS y USUARIOS."""
    # Recrear grupos con sus permisos
    for g in GRUPOS:
        grupo, _ = Group.objects.get_or_create(name=g['name'])
        for codename in g.get('permisos', []):
            try:
                perm = Permission.objects.get(codename=codename)
                grupo.permissions.add(perm)
            except Permission.DoesNotExist:
                print(f'  Permiso no encontrado: {codename}')
        print(f'Grupo recreado: {g["name"]}')

    # Recrear usuarios (create_user genera el hash de la contraseña automáticamente)
    for u in USUARIOS:
        user = User.objects.create_user(
            username=u['username'],
            password=u['password'],
        )
        user.is_staff = u.get('is_staff', False)
        user.is_superuser = u.get('is_superuser', False)
        user.is_active = True
        user.save()
        for gname in u['grupos']:
            try:
                grupo = Group.objects.get(name=gname)
                user.groups.add(grupo)
            except Group.DoesNotExist:
                print(f'  Grupo no encontrado: {gname}')
        print(f'Usuario recreado: {u["username"]}')


def poblar_personal():
    """Crea un Personal por cada sector."""
    sectores = [
        ('Porteria 2', 'Diego', 'Lirola', '5020'),
        ('Inspeccion Quimica', 'Clarisa', 'Gomez', '5021'),
        ('Almacen PQ', 'Eugenio', 'Lopez', '5022'),
        ('SHYMA', 'Lalo', 'Garcia', '5038'),
        ('PAMO', 'Esteban', 'Quito', '5023'),
        ('PSUL', 'Edgardo', 'Lambes', '5024'),
    ]
    for sector, nombre, apellido, legajo in sectores:
        Personal.objects.get_or_create(
            legajo=legajo,
            defaults={
                'sector': sector,
                'nombre': nombre,
                'apellido': apellido,
            }
        )
        print(f'Personal creado: {legajo}-{nombre} {apellido} ({sector})')


def poblar_transporte():
    """Crea 3 empresas de transporte con 2 camiones, 2 semis y 2 choferes cada una."""
    empresas = [
        {
            'nombre': 'Transporte del Sur',
            'camiones': [('Mercedes-Benz', 'AA100AA'), ('Volvo', 'AA200AA')],
            'semis': ['AA101AA', 'AA201AA'],
            'choferes': [('Alberto', 'Secundino', '20256654'), ('Carlos', 'Perez', '30123456')],
        },
        {
            'nombre': 'Cargas del Norte',
            'camiones': [('Scania', 'BB100BB'), ('Iveco', 'BB200BB')],
            'semis': ['BB101BB', 'BB201BB'],
            'choferes': [('Jorge', 'Ramirez', '28123456'), ('Luis', 'Fernandez', '31123456')],
        },
        {
            'nombre': 'Logistica Central',
            'camiones': [('Ford', 'CC100CC'), ('MAN', 'CC200CC')],
            'semis': ['CC101CC', 'CC201CC'],
            'choferes': [('Miguel', 'Torres', '27123456'), ('Raul', 'Diaz', '32123456')],
        },
    ]

    for emp in empresas:
        transporte, _ = Transporte.objects.get_or_create(nombre=emp['nombre'])
        print(f'Transporte creado: {emp["nombre"]}')

        for marca, patente in emp['camiones']:
            Camion.objects.get_or_create(
                patente=patente,
                defaults={
                    'transporte': transporte,
                    'marca': marca,
                    'vencimiento_seguro': date.today() + timedelta(days=365),
                }
            )
            print(f'  Camion: {marca} {patente}')

        for patente in emp['semis']:
            Semi.objects.get_or_create(
                patente=patente,
                defaults={
                    'transporte': transporte,
                    'vencimiento_seguro': date.today() + timedelta(days=365),
                }
            )
            print(f'  Semi: {patente}')

        for nombre, apellido, dni in emp['choferes']:
            Conductor.objects.get_or_create(
                dni=dni,
                defaults={
                    'transporte': transporte,
                    'nombre': nombre,
                    'apellido': apellido,
                    'vencimiento_carnet': date.today() + timedelta(days=365),
                }
            )
            print(f'  Conductor: {nombre} {apellido} (DNI {dni})')


def poblar_proveedores():
    """Crea al menos 4 proveedores ficticios y productos."""
    productos = ['Azufre Líquido', 'Azufre sólido', 'Amoníaco', 'Hipoclorito']
    for nombre in productos:
        Producto.objects.get_or_create(producto=nombre)
    print('Productos creados.')

    proveedores = ['YPF', 'Petroquimica Sur', 'Quimica del Valle', 'Agroinsumos SA']
    for nombre in proveedores:
        Proveedor.objects.get_or_create(nombre=nombre)
        print(f'Proveedor creado: {nombre}')


def main():
    print('=== Eliminando base de datos y migrando ===')
    eliminar_y_migrar()

    print('=== Recreando usuarios y grupos ===')
    recrear_usuarios_grupos()

    print('=== Poblando Personal ===')
    #poblar_personal()

    print('=== Poblando Transporte ===')
    #poblar_transporte()

    print('=== Poblando Proveedores ===')
    #poblar_proveedores()

    print('=== RESET COMPLETADO ===')


if __name__ == '__main__':
    main()