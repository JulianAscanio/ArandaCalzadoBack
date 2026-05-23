from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Material ,Product, Movement
from .serializers import MaterialSerializer, ProductSerializer, MovementSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    # permission_classes = [IsAuthenticated] # Comentado temporalmente para facilitar la conexión con el front. Descomentar en producción.

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class MovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movement.objects.all().order_by('-date', '-id')
    serializer_class = MovementSerializer