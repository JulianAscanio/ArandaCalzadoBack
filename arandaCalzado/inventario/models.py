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
