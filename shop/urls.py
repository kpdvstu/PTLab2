from django.urls import path
from . import views# Или from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'), # Новый путь
    path('cart/', views.cart_view, name='cart'),                  # Новый путь

]