from django.db import models

class Material(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    stock = models.FloatField(default=0)
    min_stock = models.FloatField(default=0)
    max_stock = models.FloatField(default=1000)
    unit = models.CharField(max_length=50)
    last_entry = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    reference = models.CharField(max_length=100, default="")
    heel_height = models.CharField(max_length=50, default="")
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    available_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.reference})"

class Movement(models.Model):
    MOVEMENT_TYPES = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('creación', 'Creación'),
        ('eliminación', 'Eliminación'),
    )
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True, related_name='movements')
    material_name = models.CharField(max_length=255)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.FloatField(default=0)
    reason = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.material_name} - {self.movement_type} - {self.quantity}"

from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

@receiver(pre_save, sender=Material)
def track_material_stock_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Material.objects.get(pk=instance.pk)
            old_stock = old_instance.stock
            new_stock = instance.stock
            if old_stock != new_stock:
                diff = new_stock - old_stock
                instance._stock_diff = diff
        except Material.DoesNotExist:
            pass

@receiver(post_save, sender=Material)
def log_material_movement(sender, instance, created, **kwargs):
    if created:
        Movement.objects.create(
            material=instance,
            material_name=instance.name,
            movement_type='creación',
            quantity=instance.stock,
            reason=getattr(instance, '_movement_reason', None) or "Creación de material"
        )
    else:
        diff = getattr(instance, '_stock_diff', None)
        if diff is not None and diff != 0:
            mov_type = 'entrada' if diff > 0 else 'salida'
            reason = getattr(instance, '_movement_reason', None) or ("Ajuste de stock" if diff > 0 else "Retiro de material")
            Movement.objects.create(
                material=instance,
                material_name=instance.name,
                movement_type=mov_type,
                quantity=abs(diff),
                reason=reason
            )

@receiver(pre_delete, sender=Material)
def log_material_deletion(sender, instance, **kwargs):
    Movement.objects.create(
        material=None,
        material_name=instance.name,
        movement_type='eliminación',
        quantity=instance.stock,
        reason="Eliminación de material"
    )