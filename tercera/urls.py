from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, OrdenViewSet, listar_productos, carrito, agregar_al_carrito, historial_pedidos

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'ordenes', OrdenViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('productos/', listar_productos, name='listar_productos'),
    path('carrito/', carrito, name='carrito'),
    path('agregar_al_carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('historial_pedidos/', historial_pedidos, name='historial_pedidos'),
]
