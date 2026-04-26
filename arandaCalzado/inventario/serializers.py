from rest_framework import serializers
from .models import Material

class MaterialSerializer(serializers.ModelSerializer):
    minStock = serializers.FloatField(source='min_stock')
    maxStock = serializers.FloatField(source='max_stock')
    lastEntry = serializers.DateField(source='last_entry', format="%d de %b de %Y")

    class Meta:
        model = Material
        fields = ['id', 'name', 'category', 'stock', 'minStock', 'maxStock', 'unit', 'lastEntry']
