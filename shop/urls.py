from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buy/<int:product_id>/', views.PurchaseCreate.as_view(), name='buy'),
    path('order/<int:purchase_id>/', views.order, name='order'),
    path('orders', views.orders, name='orders'),
]
