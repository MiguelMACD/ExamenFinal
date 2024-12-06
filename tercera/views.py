from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Producto, Orden, OrdenProducto
from .serializers import ProductoSerializer, OrdenSerializer, OrdenProductoSerializer


# API CRUD para productos
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


# API para crear órdenes y actualizar el stock
class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

    @action(detail=False, methods=['post'])
    def realizar_pedido(self, request):
        productos_data = request.data.get('productos')
        total = 0
        productos = []

        for item in productos_data:
            producto = get_object_or_404(Producto, id=item['producto'])
            cantidad = item['cantidad']

            if producto.cantidad_disponible < cantidad:
                return Response({"error": "Cantidad insuficiente para el producto: " + producto.nombre}, status=400)

            # Actualizar stock
            producto.cantidad_disponible -= cantidad
            producto.save()

            total += producto.precio * cantidad

            # Crear la relación en la orden
            orden_producto = OrdenProducto.objects.create(
                producto=producto,
                cantidad=cantidad,
                precio=producto.precio
            )
            productos.append(orden_producto)

        # Crear la orden
        orden = Orden.objects.create(
            usuario=request.user,
            total=total
        )
        orden.productos.set(productos)
        orden.save()

        return Response({"message": "Pedido realizado correctamente", "orden_id": orden.id})


# Vistas HTML
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'tercera/productos.html', {'productos': productos})


def carrito(request):
    # Aquí se podría almacenar el carrito en la sesión
    if 'carrito' not in request.session:
        request.session['carrito'] = []
    carrito_items = request.session['carrito']
    total = sum(item['precio'] * item['cantidad'] for item in carrito_items)
    return render(request, 'tercera/carrito.html', {'carrito': carrito_items, 'total': total})


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if 'carrito' not in request.session:
        request.session['carrito'] = []
    
    carrito = request.session['carrito']
    for item in carrito:
        if item['producto_id'] == producto_id:
            item['cantidad'] += 1
            break
    else:
        carrito.append({'producto_id': producto.id, 'nombre': producto.nombre, 'precio': str(producto.precio), 'cantidad': 1})
    
    request.session.modified = True
    return HttpResponseRedirect('/productos/')


def historial_pedidos(request):
    ordenes = Orden.objects.filter(usuario=request.user)
    return render(request, 'tercera/historial_pedidos.html', {'ordenes': ordenes})
