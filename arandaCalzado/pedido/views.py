from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date
from .models import Order, OrderItem
from .serializers import PedidoSerializer, ProductionOrderSerializer
from inventario.models import Material

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all() 
    serializer_class = PedidoSerializer

class ProductionViewSet(viewsets.ModelViewSet):
    serializer_class = ProductionOrderSerializer

    def get_queryset(self):
        # When listing, return only orders launched for production (operario is not empty)
        if self.action in ['list']:
            return Order.objects.filter(
                status__in=['pending', 'in_production', 'finished']
            ).exclude(operario__isnull=True).exclude(operario='')
        # For other actions (like retrieve, custom detail actions), allow locating any order
        return Order.objects.all()

    def create(self, request, *args, **kwargs):
        # Interceptamos POST a /api/produccion/ para evitar el error 500
        # Si el frontend envía el ID del pedido en el body, lo procesamos.
        order_id = request.data.get('id') or request.data.get('order_id') or request.data.get('pedido_id')
        
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.operario = request.data.get('operario', order.operario)
                order.fecha_inicio = request.data.get('fecha_inicio', date.today())
                order.status = 'pending'
                order.save()
                return Response({"status": "order launched for production", "id": order.id}, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                return Response({"error": f"No se encontró el pedido con ID {order_id}"}, status=status.HTTP_404_NOT_FOUND)
                
        return Response(
            {"error": "Falta el ID del pedido. Asegúrate de enviar el 'id' del pedido en el formulario."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Custom action to list pending sales orders that can be launched
    @action(detail=False, methods=['get'])
    def pedidos_pendientes(self, request):
        orders = Order.objects.filter(status='pending', operario__isnull=True) | Order.objects.filter(status='pending', operario='')
        data = []
        for order in orders:
            items_desc = ", ".join([f"{item.quantity} pares de {item.product.name} (Talla: {item.size})" for item in order.items.all()])
            data.append({
                "id": str(order.id),
                "descripcion": f"Pedido #{order.id} - {items_desc}" if items_desc else f"Pedido #{order.id} (Sin productos)"
            })
        return Response(data)

    # Custom action to initiate production (either launch order or start fabrication with materials)
    @action(detail=True, methods=['post'])
    def iniciar_produccion(self, request, pk=None):
        order = self.get_object()
        data = request.data
        
        # Scenario A: Launching the order from NewProductionPage
        if 'operario' in data:
            order.operario = data.get('operario')
            order.fecha_inicio = data.get('fecha_inicio') or date.today()
            order.status = 'pending'  # Make sure it's pending in production
            order.save()
            return Response({"status": "order launched for production"})
            
        # Scenario B: Starting fabrication with materials from ProductionModal
        elif 'material' in data:
            material_category = data.get('material')
            qty = float(data.get('cantidad', 0))
            obs = data.get('observaciones', '')
            
            # Find material by category
            material_obj = Material.objects.filter(category__iexact=material_category).first()
            if not material_obj:
                material_obj = Material.objects.filter(name__icontains=material_category).first()
                
            if not material_obj:
                return Response(
                    {"error": f"No se encontró material en la categoría/nombre '{material_category}'"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            if material_obj.stock < qty:
                return Response(
                    {"error": f"Stock insuficiente para '{material_obj.name}'. Disponible: {material_obj.stock}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Deduct stock and set reason for tracking
            material_obj.stock -= qty
            material_obj._movement_reason = f"Consumo producción orden #{order.id}"
            material_obj.save()
            
            # Update order details
            order.material_usado = material_obj
            order.cantidad_usada = qty
            order.observaciones_produccion = obs
            order.status = 'in_production'
            order.save()
            
            return Response({"status": "production started"})
            
        else:
            return Response(
                {"error": "Datos inválidos para iniciar producción"},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Custom action to finalize production (marks as finished and increases product available stock)
    @action(detail=True, methods=['post'])
    def finalizar_produccion(self, request, pk=None):
        order = self.get_object()
        
        if order.status != 'in_production':
            return Response(
                {"error": "La orden no está en producción y no se puede finalizar"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        order.status = 'finished'
        order.save()
        
        # Increase product stocks
        for item in order.items.all():
            product = item.product
            product.available_stock += item.quantity
            product.save()
            
        return Response({"status": "production finished, product stock updated"})