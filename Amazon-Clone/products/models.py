from django.db import models
from users.models import User

# Create your models here.


class Products(models.Model):
    title = models.CharField(max_length=100)
    image = models.URLField()
    description = models.TextField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    price = models.FloatField()

    def __str__(self):
        return f"{self.id}"


class Comments(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(blank=True)
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment")

    def __str__(self) -> str:
        return f"{self.comment}"


class Cart(models.Model):
    product = models.ManyToManyField(
        Products, related_name="cart", through="Cart_Handler")
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cart")

    def __str__(self) -> str:
        return f"{self.buyer}"


class Cart_Handler(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.cart}"


class Orders(models.Model):
    product = models.ManyToManyField(
        Products, related_name="payments", through="Orders_Handler")
    payment_id = models.CharField(max_length=50, null=True, blank=True)
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders")
    timestamp = models.CharField(max_length=50, null=True)

    def __str__(self) -> str:
        return f"{self.buyer}"


class Orders_Handler(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.order}"
