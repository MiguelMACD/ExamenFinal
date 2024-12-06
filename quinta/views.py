from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from .models import Documento
from .serializers import DocumentoSerializer

# API CRUD para Documentos
class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        titulo = request.query_params.get('titulo')
        autor = request.query_params.get('autor')
        categoria = request.query_params.get('categoria')

        queryset = Documento.objects.all()

        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)
        if autor:
            queryset = queryset.filter(autor__icontains=autor)
        if categoria:
            queryset = queryset.filter(categoria__icontains=categoria)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Vistas HTML
def listar_documentos(request):
    documentos = Documento.objects.all()
    return render(request, 'quinta/listar_documentos.html', {'documentos': documentos})

def detalle_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    return render(request, 'quinta/detalle_documento.html', {'documento': documento})

def subir_documento(request):
    if request.method == 'POST':
        archivo = request.FILES['archivo']
        titulo = request.POST['titulo']
        autor = request.POST['autor']
        categoria = request.POST['categoria']
        Documento.objects.create(titulo=titulo, autor=autor, categoria=categoria, archivo=archivo)
        return redirect('listar_documentos')
    return render(request, 'quinta/subir_documento.html')
