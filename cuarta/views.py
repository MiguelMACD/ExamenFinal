from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from .models import Vehiculo, Reserva
from .serializers import VehiculoSerializer, ReservaSerializer

# API CRUD para Vehículos
class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer


# API CRUD para Reservas
class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    @action(detail=False, methods=['get'])
    def verificar_disponibilidad(self, request):
        vehiculo_id = request.query_params.get('vehiculo')
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        if not vehiculo_id or not fecha_inicio or not fecha_fin:
            return Response({"error": "Faltan parámetros."}, status=400)

        vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

        # Verificar si ya hay reservas para el vehículo en el rango de fechas
        reservas = Reserva.objects.filter(vehiculo=vehiculo, fecha_inicio__lt=fecha_fin, fecha_fin__gt=fecha_inicio)

        if reservas.exists():
            return Response({"disponible": False, "mensaje": "El vehículo no está disponible en estas fechas."}, status=200)

        return Response({"disponible": True, "mensaje": "El vehículo está disponible en estas fechas."}, status=200)

    @action(detail=False, methods=['post'])
    def realizar_reserva(self, request):
        vehiculo_id = request.data.get('vehiculo')
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')
        precio_total = request.data.get('precio_total')

        if not vehiculo_id or not fecha_inicio or not fecha_fin or not precio_total:
            return Response({"error": "Faltan parámetros."}, status=400)

        vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

        # Verificar disponibilidad antes de realizar la reserva
        reservas = Reserva.objects.filter(vehiculo=vehiculo, fecha_inicio__lt=fecha_fin, fecha_fin__gt=fecha_inicio)

        if reservas.exists():
            return Response({"error": "El vehículo no está disponible en estas fechas."}, status=400)

        # Crear la reserva
        reserva = Reserva.objects.create(
            usuario=request.user,
            vehiculo=vehiculo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            precio_total=precio_total
        )

        return Response({"message": "Reserva realizada correctamente", "reserva_id": reserva.id}, status=201)


# Vistas HTML
def listar_vehiculos(request):
    vehiculos = Vehiculo.objects.filter(disponibilidad=True)
    return render(request, 'cuarta/vehiculos.html', {'vehiculos': vehiculos})


def detalle_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    return render(request, 'cuarta/detalle_vehiculo.html', {'vehiculo': vehiculo})


def historial_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'cuarta/historial_reservas.html', {'reservas': reservas})
