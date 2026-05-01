from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Customer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer() # Quitamos el read_only=True para que acepte datos

    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'address', 'city']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer