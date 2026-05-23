from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaterialViewSet, ProductViewSet, MovementViewSet

router = DefaultRouter()
router.register(r'materiales', MaterialViewSet)
router.register(r'productos', ProductViewSet)
router.register(r'movimientos', MovementViewSet, basename='movimientos')

urlpatterns = [
    path('', include(router.urls)),
]