from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Proyecto, Tarea
from .serializers import ProyectoSerializer, TareaSerializer


# APIs REST
class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer


class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        tarea = self.get_object()
        nuevo_estado = request.data.get('estado')
        if nuevo_estado in dict(Tarea.ESTADO_CHOICES):
            tarea.estado = nuevo_estado
            tarea.save()
            return Response({'status': 'estado actualizado'})
        return Response({'error': 'Estado no válido'}, status=400)


# Vistas HTML
def listar_proyectos(request):
    """
    Página para listar todos los proyectos.
    """
    proyectos = Proyecto.objects.all()
    return render(request, 'primera/proyectos.html', {'proyectos': proyectos})


def detalle_proyecto(request, id):
    """
    Página de detalle de un proyecto con su lista de tareas.
    """
    proyecto = get_object_or_404(Proyecto, id=id)
    tareas = proyecto.tareas.all()
    return render(request, 'primera/detalle_proyecto.html', {'proyecto': proyecto, 'tareas': tareas})


def agregar_tarea(request, proyecto_id):
    """
    Formulario para agregar una nueva tarea a un proyecto.
    """
    if request.method == "POST":
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
        Tarea.objects.create(
            proyecto=proyecto,
            titulo=request.POST['titulo'],
            descripcion=request.POST['descripcion'],
            fecha_vencimiento=request.POST['fecha_vencimiento'],
        )
        return HttpResponseRedirect(f'/proyectos/{proyecto_id}/')
