from rest_framework import serializers
from .models import Order
from usuarios.models import Customer
from usuarios.serializers import CustomerSerializer # Tu serializer de cliente

class PedidoSerializer(serializers.ModelSerializer):
    # Esto permite VER los detalles del cliente en un GET
    customer_detail = CustomerSerializer(source='customer', read_only=True)
    
    # Esto permite ENVIAR el ID del cliente en un POST
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), 
        write_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id', 
            'customer',        # Para escribir (POST)
            'customer_detail', # Para leer (GET)
            'created_at', 
            'status', 
            'total_amount', 
            'additional_info'
        ]

    def create(self, validated_data):
        # El customer ya vendrá en validated_data porque es un PrimaryKeyRelatedField
        return Order.objects.create(**validated_data)