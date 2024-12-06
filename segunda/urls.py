from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HospitalViewSet, MedicoViewSet, PacienteViewSet, listar_hospitales, detalle_medico, registrar_paciente

router = DefaultRouter()
router.register(r'hospitales', HospitalViewSet)
router.register(r'medicos', MedicoViewSet)
router.register(r'pacientes', PacienteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('hospitales/', listar_hospitales, name='listar_hospitales'),
    path('medico/<int:id>/', detalle_medico, name='detalle_medico'),
    path('medico/<int:medico_id>/registrar_paciente/', registrar_paciente, name='registrar_paciente'),
]
