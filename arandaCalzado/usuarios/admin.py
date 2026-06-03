from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'city', 'address')
    search_fields = ('full_name', 'phone')