from django.urls import path

from . import views


app_name = 'stripe_app'

urlpatterns = [
    path('', views.index, name='items'),
    path('item/<int:pk>/', views.get_item, name='get_item'),
    path('buy/<int:pk>/', views.create_checkout_session, name='buy'),
    path('success/', views.success, name='success'),
    path('canceled/', views.canceled, name='canceled'),
]
