from datetime import date
import datetime
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.http import QueryDict
from stripe.api_resources import product

from .models import*
from .serializers import*
from users.models import User

# Create your views here.


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = CommentsSerializer

    def get_queryset(self):
        queryset = Comments.objects.filter(
            product=self.request.query_params['product'])
        return queryset

    def create(self, request, *args, **kwargs):
        product_id = request.data['product']
        product_instance = Products.objects.get(pk=product_id)
        comment = request.data['comment']
        new_comment = Comments.objects.create(
            product=product_instance, comment=comment, commenter=request.user)
        new_comment.save()
        serializer = CommentsSerializer(new_comment)
        return Response(serializer.data)


class CartViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = CartSerializer

    def get_queryset(self):
        queryset = Cart.objects.filter(
            buyer=self.request.user)
        if not queryset:
            new_cart = Cart.objects.create(buyer=self.request.user)
            new_cart.save()
            queryset = Cart.objects.filter(
                buyer=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        product_id = request.data['product']
        product_instance = Products.objects.get(pk=product_id)
        cart_id = request.data['cart']
        cart_instance = Cart.objects.get(pk=cart_id)
        item = Cart_Handler.objects.create(
            product=product_instance, cart=cart_instance)
        item.save()
        serializer = Cart_HandlerSerializer(item)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # request.data return differnet object in put than in other requests
        product_id = request.data['data']['product']
        data = Cart_Handler.objects.filter(
            product=product_id, cart=instance).first()
        if data:
            data.delete()
        return Response("item has been deleted")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = Cart_Handler.objects.filter(cart=instance)
        if data:
            data.delete()
        return Response("item has been deleted")


class OrdersViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = OrdersSerializer

    def get_queryset(self):
        queryset = Orders.objects.filter(
            buyer=self.request.user).order_by('-timestamp')
        return queryset

    def create(self, request, *args, **kwargs):
        products = request.data['product']
        payment_id = request.data['payment']
        timestamp = datetime.datetime.now()
        formated_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        order_instance = Orders.objects.create(
            buyer=request.user, payment_id=payment_id, timestamp=formated_timestamp)
        order_instance.save()
        for prod in products:
            product_instance = Products.objects.get(
                pk=products[str(prod)]['id'])
            new_order = Orders_Handler.objects.create(
                product=product_instance, order=order_instance)
            new_order.save()
        return Response("item has been created")
