from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductionViewSet

router = DefaultRouter()
router.register(r'', ProductionViewSet, basename='produccion')

urlpatterns = [
    path('', include(router.urls)),
]
