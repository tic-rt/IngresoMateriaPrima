from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Producto

@receiver(post_migrate)
def populate_producto(sender, **kwargs):
    # Verificar si la tabla 'Producto' está vacía
    if Producto.objects.count() == 0:
        # Si está vacía, poblarla con productos predeterminados
        Producto.objects.create(producto="Azufre Líquido")
        Producto.objects.create(producto="Azufre sólido o a granel")
        Producto.objects.create(producto="Amoníaco")
        Producto.objects.create(producto="Hipoclorito")