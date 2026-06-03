from rest_framework import viewsets
from django.db.models import Count, Sum
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.annotate(
        annotated_orders_count=Count('orders'),
        annotated_total_purchased=Sum('orders__total_amount')
    ).order_by('-id')
    serializer_class = CustomerSerializer