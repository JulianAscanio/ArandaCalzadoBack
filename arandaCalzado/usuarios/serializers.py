from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    orders_count = serializers.SerializerMethodField()
    total_purchased = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'phone', 'address', 'city', 'email', 'orders_count', 'total_purchased']

    def get_orders_count(self, obj):
        return getattr(obj, 'annotated_orders_count', 0)

    def get_total_purchased(self, obj):
        return getattr(obj, 'annotated_total_purchased', 0) or 0