from django.contrib import admin
from .models import Producto, Orden, OrdenProducto

admin.site.register(Producto)
admin.site.register(Orden)
admin.site.register(OrdenProducto)
