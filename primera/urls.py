from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProyectoViewSet, TareaViewSet, listar_proyectos, detalle_proyecto, agregar_tarea

# Enrutador para las APIs REST
router = DefaultRouter()
router.register(r'proyectos', ProyectoViewSet)
router.register(r'tareas', TareaViewSet)

# URLs para vistas HTML
urlpatterns = [
    path('', include(router.urls)),  # APIs REST
    path('proyectos/', listar_proyectos, name='listar_proyectos'),  # Lista de proyectos
    path('proyectos/<int:id>/', detalle_proyecto, name='detalle_proyecto'),  # Detalle de proyecto
    path('proyectos/<int:proyecto_id>/agregar_tarea/', agregar_tarea, name='agregar_tarea'),  # Agregar tarea
]
