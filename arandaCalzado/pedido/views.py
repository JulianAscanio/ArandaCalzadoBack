from rest_framework import viewsets
from .models import Order  
from .serializers import PedidoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all() 
    serializer_class = PedidoSerializer