import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arandaCalzado.settings')
django.setup()

from django.contrib.auth.models import User
from inventario.models import Material

# Create user
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
    print("User 'admin' created with password 'admin123'")

# Create materials
materials = [
    {"name": "Cuero natural café", "category": "Cuero", "stock": 320, "min_stock": 100, "max_stock": 500, "unit": "dm²"},
    {"name": "Cuero sintético negro", "category": "Cuero", "stock": 85, "min_stock": 120, "max_stock": 300, "unit": "dm²"},
    {"name": "Suelas de caucho N°36", "category": "Suelas", "stock": 45, "min_stock": 50, "max_stock": 100, "unit": "pares"},
    {"name": "Pegante especial", "category": "Adhesivos", "stock": 12, "min_stock": 10, "max_stock": 50, "unit": "litros"},
]

for mat in materials:
    Material.objects.update_or_create(name=mat['name'], defaults=mat)
print("Materials seeded successfully.")
