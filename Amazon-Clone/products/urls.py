from django.db import router
from rest_framework import routers, urlpatterns
from django.urls import path
from django.conf.urls import url, include

from .views import*

router = routers.DefaultRouter()
router.register('products', ProductsViewSet, 'products')
router.register('comments', CommentsViewSet, 'comments')
router.register('cart', CartViewSet, 'cart')
# router.register('cart_handler', Cart_HandlerViewSet, 'cart_handle')
router.register('orders', OrdersViewSet, 'orders')

urlpatterns = router.urls
