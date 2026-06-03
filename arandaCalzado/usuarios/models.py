from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.full_name