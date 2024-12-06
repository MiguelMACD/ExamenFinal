from rest_framework import serializers
from .models import Producto, Orden, OrdenProducto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class OrdenProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenProducto
        fields = '__all__'


class OrdenSerializer(serializers.ModelSerializer):
    productos = OrdenProductoSerializer(many=True)

    class Meta:
        model = Orden
        fields = ['id', 'usuario', 'fecha', 'total', 'productos']
