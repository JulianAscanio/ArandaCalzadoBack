from django.contrib import admin
from .models import Material, Product

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'stock', 'unit', 'last_entry')
    list_filter = ('category',)
    search_fields = ('name','stock')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference', 'heel_height', 'price', 'available_stock', 'material', 'image')
    list_filter = ('heel_height', 'material')
    search_fields = ('name', 'reference')