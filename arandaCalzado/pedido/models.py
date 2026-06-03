from django.db import models
from usuarios.models import Customer
from inventario.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('in_production', 'En Producción'),
        ('finished', 'Terminado'),
        ('sent', 'Enviado'),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    additional_info = models.TextField(blank=True, null=True)
    
    # Campos para el control de producción
    operario = models.CharField(max_length=255, blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    material_usado = models.ForeignKey('inventario.Material', on_delete=models.SET_NULL, blank=True, null=True, related_name='production_orders')
    cantidad_usada = models.FloatField(blank=True, null=True)
    observaciones_produccion = models.TextField(blank=True, null=True)

    def __str__(self):
        customer_name = self.customer.user.username if self.customer.user else self.customer.full_name
        return f"Order {self.id} - {customer_name}"

class OrderItem(models.Model):
    """
    intermedia
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.IntegerField(default=35)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Talla: {self.size})"