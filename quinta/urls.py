from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentoViewSet, listar_documentos, detalle_documento, subir_documento

router = DefaultRouter()
router.register(r'documentos', DocumentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('documentos/', listar_documentos, name='listar_documentos'),
    path('documento/<int:documento_id>/', detalle_documento, name='detalle_documento'),
    path('subir/', subir_documento, name='subir_documento'),
]
