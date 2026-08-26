import os
import django
from datetime import date, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IngresoMateriaPrima.settings")
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User, Group, Permission
from personal.models import Personal
from transporte.models import Transporte, Camion, Semi, Conductor
from proveedores.models import Proveedor, Producto


GRUPOS = [
    {
        "name": "G_Porteria2",
        "permisos": [
            "add_hdr", "change_hdr", "view_hdr",
            "add_personal", "change_personal", "view_personal",
            "add_egreso", "change_egreso", "view_egreso",
            "add_epp", "view_epp",
            "add_ingreso", "change_ingreso", "view_ingreso",
            "add_camion", "change_camion", "view_camion",
            "add_conductor", "change_conductor", "view_conductor",
            "add_semi", "change_semi", "view_semi",
            "add_transporte", "change_transporte", "view_transporte",
            "add_producto", "view_producto",
            "add_proveedor", "view_proveedor",
            "add_proveedorproducto", "view_proveedorproducto",
        ],
    },
    {
        "name": "G_Balanza",
        "permisos": [
            "add_balanza", "change_balanza", "view_balanza",
            "change_hdr", "view_hdr",
            "add_personal", "change_personal", "view_personal",
            "add_egreso", "change_egreso", "view_egreso",
            "change_ingreso", "view_ingreso",
            "add_proveedor", "view_proveedor",
            "add_producto", "view_producto",
            "add_proveedorproducto", "view_proveedorproducto",
        ],
    },
    {
        "name": "G_Laboratorio",
        "permisos": [
            "change_hdr", "view_hdr",
            "add_inspeccion", "view_inspeccion",
            "add_personal", "change_personal", "view_personal",
            "change_ingreso", "view_ingreso",
        ],
    },
    {
        "name": "G_Pamo",
        "permisos": [
            "change_hdr", "view_hdr",
            "add_pamopsul", "change_pamopsul", "view_pamopsul", "delete_pamopsul",
            "add_personal", "change_personal", "view_personal",
            "change_ingreso", "view_ingreso",
        ],
    },
    {
        "name": "G_Psul",
        "permisos": [
            "change_hdr", "view_hdr",
            "add_pamopsul", "change_pamopsul", "view_pamopsul",
            "add_personal", "view_personal",
            "change_ingreso", "view_ingreso",
        ],
    },
    {
        "name": "G_Shyma",
        "permisos": [
            "change_hdr", "view_hdr",
            "add_personal", "view_personal",
            "view_ingreso",
        ],
    },
]


# Las contraseñas NO se guardan en el código.
# Deben existir como variables de entorno en .env.
USUARIOS = [
    {
        "username": "Tic",
        "password_env": "APP_USER_TIC_PASSWORD",
        "is_staff": True,
        "is_superuser": True,
        "grupos": [],
    },
    {
        "username": "Porteria2",
        "password_env": "APP_USER_PORTERIA2_PASSWORD",
        "grupos": ["G_Porteria2"],
    },
    {
        "username": "Shyma",
        "password_env": "APP_USER_SHYMA_PASSWORD",
        "grupos": ["G_Shyma"],
    },
    {
        "username": "Balanza",
        "password_env": "APP_USER_BALANZA_PASSWORD",
        "grupos": ["G_Balanza"],
    },
    {
        "username": "Laboratorio",
        "password_env": "APP_USER_LABORATORIO_PASSWORD",
        "grupos": ["G_Laboratorio"],
    },
    {
        "username": "Pamo",
        "password_env": "APP_USER_PAMO_PASSWORD",
        "grupos": ["G_Pamo"],
    },
    {
        "username": "Psul",
        "password_env": "APP_USER_PSUL_PASSWORD",
        "grupos": ["G_Psul"],
    },
]


def validar_variables_usuarios():
    """Verifica que existan las contraseñas requeridas en las variables de entorno."""
    faltantes = [
        u["password_env"]
        for u in USUARIOS
        if not os.environ.get(u["password_env"])
    ]

    if faltantes:
        variables = "\n  - ".join(faltantes)
        raise RuntimeError(
            "Faltan variables de entorno para crear/actualizar usuarios:\n"
            f"  - {variables}\n"
            "Definilas en el archivo .env antes de ejecutar este script."
        )


def aplicar_migraciones():
    """
    Aplica las migraciones Django sobre la base configurada en settings.py.
    No elimina la base de datos ni borra datos existentes.
    Funciona con MySQL y otros motores soportados por Django.
    """
    print("=== Aplicando migraciones ===")
    call_command("migrate", verbosity=1)
    print("Migraciones aplicadas.")


def obtener_permiso(codename):
    """
    Busca un permiso por codename.
    Si no existe o el codename es ambiguo, no asigna nada y lo informa.
    """
    permisos = Permission.objects.filter(codename=codename)

    if not permisos.exists():
        print(f"  ADVERTENCIA: permiso no encontrado: {codename}")
        return None

    if permisos.count() > 1:
        apps = ", ".join(
            f"{p.content_type.app_label}.{p.content_type.model}"
            for p in permisos.select_related("content_type")
        )
        print(
            f"  ADVERTENCIA: permiso ambiguo '{codename}' "
            f"(coincide con: {apps}). No se asignó."
        )
        return None

    return permisos.first()


def crear_actualizar_grupos():
    """
    Crea o actualiza los grupos.
    Los permisos del grupo quedan exactamente como están definidos en GRUPOS.
    """
    print("=== Creando/actualizando grupos y permisos ===")

    for definicion in GRUPOS:
        grupo, creado = Group.objects.get_or_create(name=definicion["name"])

        permisos_validos = []
        for codename in definicion["permisos"]:
            permiso = obtener_permiso(codename)
            if permiso is not None:
                permisos_validos.append(permiso)

        grupo.permissions.set(permisos_validos)

        estado = "creado" if creado else "actualizado"
        print(f'Grupo {estado}: {grupo.name} ({len(permisos_validos)} permisos)')


def crear_actualizar_usuarios():
    """
    Crea o actualiza los usuarios definidos en USUARIOS.
    Es idempotente: puede ejecutarse varias veces sin duplicar usuarios.
    """
    print("=== Creando/actualizando usuarios ===")

    for definicion in USUARIOS:
        password = os.environ[definicion["password_env"]]

        user, creado = User.objects.get_or_create(
            username=definicion["username"]
        )

        user.set_password(password)
        user.is_staff = definicion.get("is_staff", False)
        user.is_superuser = definicion.get("is_superuser", False)
        user.is_active = True
        user.save()

        grupos = Group.objects.filter(name__in=definicion["grupos"])
        user.groups.set(grupos)

        estado = "creado" if creado else "actualizado"
        print(f'Usuario {estado}: {user.username}')


def poblar_personal():
    """Crea un Personal por cada sector. Datos opcionales de prueba/iniciales."""
    sectores = [
        ("Porteria 2", "Diego", "Lirola", "5020"),
        ("Inspeccion Quimica", "Clarisa", "Gomez", "5021"),
        ("Almacen PQ", "Eugenio", "Lopez", "5022"),
        ("SHYMA", "Lalo", "Garcia", "5038"),
        ("PAMO", "Esteban", "Quito", "5023"),
        ("PSUL", "Edgardo", "Lambes", "5024"),
    ]

    for sector, nombre, apellido, legajo in sectores:
        _, creado = Personal.objects.get_or_create(
            legajo=legajo,
            defaults={
                "sector": sector,
                "nombre": nombre,
                "apellido": apellido,
            },
        )
        estado = "creado" if creado else "existente"
        print(f"Personal {estado}: {legajo}-{nombre} {apellido} ({sector})")


def poblar_transporte():
    """Crea datos ficticios de transporte. Uso opcional, no se ejecuta por defecto."""
    empresas = [
        {
            "nombre": "Transporte del Sur",
            "camiones": [("Mercedes-Benz", "AA100AA"), ("Volvo", "AA200AA")],
            "semis": ["AA101AA", "AA201AA"],
            "choferes": [
                ("Alberto", "Secundino", "20256654"),
                ("Carlos", "Perez", "30123456"),
            ],
        },
        {
            "nombre": "Cargas del Norte",
            "camiones": [("Scania", "BB100BB"), ("Iveco", "BB200BB")],
            "semis": ["BB101BB", "BB201BB"],
            "choferes": [
                ("Jorge", "Ramirez", "28123456"),
                ("Luis", "Fernandez", "31123456"),
            ],
        },
        {
            "nombre": "Logistica Central",
            "camiones": [("Ford", "CC100CC"), ("MAN", "CC200CC")],
            "semis": ["CC101CC", "CC201CC"],
            "choferes": [
                ("Miguel", "Torres", "27123456"),
                ("Raul", "Diaz", "32123456"),
            ],
        },
    ]

    for emp in empresas:
        transporte, _ = Transporte.objects.get_or_create(nombre=emp["nombre"])
        print(f'Transporte: {emp["nombre"]}')

        for marca, patente in emp["camiones"]:
            Camion.objects.get_or_create(
                patente=patente,
                defaults={
                    "transporte": transporte,
                    "marca": marca,
                    "vencimiento_seguro": date.today() + timedelta(days=365),
                },
            )

        for patente in emp["semis"]:
            Semi.objects.get_or_create(
                patente=patente,
                defaults={
                    "transporte": transporte,
                    "vencimiento_seguro": date.today() + timedelta(days=365),
                },
            )

        for nombre, apellido, dni in emp["choferes"]:
            Conductor.objects.get_or_create(
                dni=dni,
                defaults={
                    "transporte": transporte,
                    "nombre": nombre,
                    "apellido": apellido,
                    "vencimiento_carnet": date.today() + timedelta(days=365),
                },
            )


def poblar_proveedores():
    """Crea datos ficticios de proveedores/productos. No se ejecuta por defecto."""
    productos = ["Azufre Líquido", "Azufre sólido", "Amoníaco", "Hipoclorito"]

    for nombre in productos:
        Producto.objects.get_or_create(producto=nombre)

    proveedores = [
        "YPF",
        "Petroquimica Sur",
        "Quimica del Valle",
        "Agroinsumos SA",
    ]

    for nombre in proveedores:
        Proveedor.objects.get_or_create(nombre=nombre)


def main():
    print("=== INICIALIZACIÓN DE INGRESO MATERIA PRIMA ===")

    validar_variables_usuarios()
    aplicar_migraciones()
    crear_actualizar_grupos()
    crear_actualizar_usuarios()

    # Datos opcionales. Mantener desactivados en producción salvo decisión explícita.
    # print("=== Poblando Personal ===")
    # poblar_personal()

    # print("=== Poblando Transporte ===")
    # poblar_transporte()

    # print("=== Poblando Proveedores ===")
    # poblar_proveedores()

    print("=== INICIALIZACIÓN COMPLETADA ===")


if __name__ == "__main__":
    main()
