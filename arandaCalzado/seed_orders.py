import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arandaCalzado.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import Customer
from inventario.models import Material, Product
from pedido.models import Order, OrderItem

def run_seed():
    print("Starting data seeding...")

    # 1. Create Users & Customers
    customers_data = [
        {"username": "jdoe", "first_name": "Juan", "last_name": "Pérez", "email": "juan@example.com", "phone": "3001234567", "address": "Calle Falsa 123", "city": "Bogotá"},
        {"username": "msmith", "first_name": "María", "last_name": "Gómez", "email": "maria@example.com", "phone": "3109876543", "address": "Carrera 45 # 12-34", "city": "Medellín"},
        {"username": "cgarcia", "first_name": "Carlos", "last_name": "García", "email": "carlos@example.com", "phone": "3205556677", "address": "Avenida Siempre Viva", "city": "Cali"},
    ]

    customers_created = []
    for data in customers_data:
        user, created = User.objects.get_or_create(
            username=data["username"],
            defaults={"first_name": data["first_name"], "last_name": data["last_name"], "email": data["email"]}
        )
        if created:
            user.set_password("password123")
            user.save()
        
        customer, _ = Customer.objects.get_or_create(
            user=user,
            defaults={"phone": data["phone"], "address": data["address"], "city": data["city"]}
        )
        customers_created.append(customer)
    print(f"Created/verified {len(customers_created)} customers.")

    # 2. Create Products (Requires Materials first)
    material = Material.objects.filter(name__icontains="Cuero natural").first()
    if not material:
        material = Material.objects.create(name="Cuero natural café", category="Cuero", stock=100, unit="dm²")

    products_data = [
        {"name": "Botas Clásicas de Cuero", "price": Decimal("150000.00"), "size": 40, "available_stock": 10},
        {"name": "Zapatos Oxford Formales", "price": Decimal("120000.00"), "size": 39, "available_stock": 15},
        {"name": "Tenis Urbanos Blancos", "price": Decimal("95000.00"), "size": 42, "available_stock": 20},
        {"name": "Botines de Invierno", "price": Decimal("180000.00"), "size": 38, "available_stock": 5},
    ]

    products_created = []
    for data in products_data:
        product, _ = Product.objects.get_or_create(
            name=data["name"],
            size=data["size"],
            defaults={"price": data["price"], "material": material, "available_stock": data["available_stock"]}
        )
        products_created.append(product)
    print(f"Created/verified {len(products_created)} products.")

    # 3. Create Orders
    orders_data = [
        {"customer": customers_created[0], "status": "pending", "items": [{"product": products_created[0], "quantity": 1}, {"product": products_created[2], "quantity": 2}]},
        {"customer": customers_created[1], "status": "in_production", "items": [{"product": products_created[1], "quantity": 1}]},
        {"customer": customers_created[2], "status": "finished", "items": [{"product": products_created[3], "quantity": 1}]},
        {"customer": customers_created[0], "status": "sent", "items": [{"product": products_created[1], "quantity": 3}]},
    ]

    for data in orders_data:
        if not Order.objects.filter(customer=data["customer"], status=data["status"]).exists():
            total = sum(item["product"].price * item["quantity"] for item in data["items"])
            order = Order.objects.create(customer=data["customer"], status=data["status"], total_amount=total)
            for item in data["items"]:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    unit_price=item["product"].price
                )
    print("Created/verified test orders successfully.")

if __name__ == "__main__":
    run_seed()
