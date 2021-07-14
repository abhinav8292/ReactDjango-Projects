from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import*

from users.serializers import UserSerializer


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    commenter = UserSerializer()

    class Meta:
        model = Comments
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'


class Cart_HandlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_Handler
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(many=True)

    class Meta:
        model = Orders
        fields = '__all__'
