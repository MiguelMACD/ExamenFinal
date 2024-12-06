from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Hospital, Medico, Paciente
from .serializers import HospitalSerializer, MedicoSerializer, PacienteSerializer


# API CRUD
class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

    @action(detail=True, methods=['get'])
    def pacientes(self, request, pk=None):
        medico = self.get_object()
        pacientes = Paciente.objects.filter(medico=medico)
        serializer = PacienteSerializer(pacientes, many=True)
        return Response(serializer.data)


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


# Vistas HTML
def listar_hospitales(request):
    hospitales = Hospital.objects.all()
    return render(request, 'segunda/hospitales.html', {'hospitales': hospitales})


def detalle_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    pacientes = medico.pacientes.all()
    return render(request, 'segunda/detalle_medico.html', {'medico': medico, 'pacientes': pacientes})


def registrar_paciente(request, medico_id):
    if request.method == "POST":
        medico = get_object_or_404(Medico, id=medico_id)
        Paciente.objects.create(
            nombre=request.POST['nombre'],
            edad=request.POST['edad'],
            enfermedad_diagnosticada=request.POST['enfermedad_diagnosticada'],
            medico=medico
        )
        return HttpResponseRedirect(f'/medico/{medico_id}/')
