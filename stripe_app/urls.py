from django.urls import path

from . import views


app_name = 'stripe_app'

urlpatterns = [
    path('', views.index, name='items'),
    path('item/<int:pk>/', views.get_item, name='get_item'),
    path('buy_items/', views.create_checkout_session, name='buy'),
    path('success/', views.success, name='success'),
    path('canceled/', views.canceled, name='canceled'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:pk>/', views.item_clear, name='item_clear'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
]
