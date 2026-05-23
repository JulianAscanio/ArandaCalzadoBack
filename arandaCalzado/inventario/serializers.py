from rest_framework import serializers
from .models import Material, Product, Movement

class MaterialSerializer(serializers.ModelSerializer):
    minStock = serializers.FloatField(source='min_stock', required=False)
    maxStock = serializers.FloatField(source='max_stock', required=False)
    lastEntry = serializers.DateField(source='last_entry', format="%d de %b de %Y", read_only=True)
    reason = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    name = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    unit = serializers.CharField(required=False)
    stock = serializers.FloatField(required=False)

    class Meta:
        model = Material
        fields = ['id', 'name', 'category', 'stock', 'minStock', 'maxStock', 'unit', 'lastEntry', 'reason']

    def update(self, instance, validated_data):
        reason = validated_data.pop('reason', None)
        if reason:
            instance._movement_reason = reason
        return super().update(instance, validated_data)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1

class MovementSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d de %b de %Y, %I:%M %p", read_only=True)
    materialName = serializers.CharField(source='material_name', read_only=True)
    movementType = serializers.CharField(source='movement_type', read_only=True)

    class Meta:
        model = Movement
        fields = ['id', 'material', 'materialName', 'movementType', 'quantity', 'reason', 'date']