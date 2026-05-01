from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Material ,Product
from .serializers import MaterialSerializer, ProductSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    # permission_classes = [IsAuthenticated] # Comentado temporalmente para facilitar la conexión con el front. Descomentar en producción.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer