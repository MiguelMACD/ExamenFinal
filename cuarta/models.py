from django.db import models
from django.contrib.auth.models import User

class Vehiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    año = models.IntegerField()
    capacidad = models.IntegerField()
    disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.año})"


class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Reserva {self.id} - {self.usuario.username} - {self.vehiculo.modelo} ({self.fecha_inicio} - {self.fecha_fin})"
