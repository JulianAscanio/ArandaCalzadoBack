from rest_framework import serializers
from .models import Order, OrderItem
from usuarios.models import Customer
from usuarios.serializers import CustomerSerializer
from inventario.models import Product
from inventario.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), 
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_detail', 'quantity', 'unit_price']

class PedidoSerializer(serializers.ModelSerializer):
    # Esto permite VER los detalles del cliente en un GET
    customer_detail = CustomerSerializer(source='customer', read_only=True)
    
    # Esto permite ENVIAR el ID del cliente en un POST
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), 
        write_only=True
    )
    
    items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = [
            'id', 
            'customer',        # Para escribir (POST)
            'customer_detail', # Para leer (GET)
            'created_at', 
            'status', 
            'total_amount', 
            'additional_info',
            'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
        
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
        return instance