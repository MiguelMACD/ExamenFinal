from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculoViewSet, ReservaViewSet, listar_vehiculos, detalle_vehiculo, historial_reservas

router = DefaultRouter()
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'reservas', ReservaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('vehiculos/', listar_vehiculos, name='listar_vehiculos'),
    path('vehiculo/<int:vehiculo_id>/', detalle_vehiculo, name='detalle_vehiculo'),
    path('historial_reservas/', historial_reservas, name='historial_reservas'),
]

