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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.IntegerField()
    # Relación con Material
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, related_name='products')
    available_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} (Size: {self.size})"