from django.db import models

class Hospital(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre


class Medico(models.Model):
    nombre = models.CharField(max_length=200)
    especialidad = models.CharField(max_length=200)
    hospital = models.ForeignKey(Hospital, related_name='medicos', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.especialidad}"


class Paciente(models.Model):
    nombre = models.CharField(max_length=200)
    edad = models.IntegerField()
    enfermedad_diagnosticada = models.TextField()
    medico = models.ForeignKey(Medico, related_name='pacientes', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre
