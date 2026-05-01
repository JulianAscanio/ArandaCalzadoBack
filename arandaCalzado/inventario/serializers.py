from rest_framework import serializers
from .models import Material, Product

class MaterialSerializer(serializers.ModelSerializer):
    minStock = serializers.FloatField(source='min_stock')
    maxStock = serializers.FloatField(source='max_stock')
    lastEntry = serializers.DateField(source='last_entry', format="%d de %b de %Y")

    class Meta:
        model = Material
        fields = ['id', 'name', 'category', 'stock', 'minStock', 'maxStock', 'unit', 'lastEntry']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1