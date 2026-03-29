from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('pago/<str:order_number>/', views.payment_page, name='payment'),
    path('confirmacion/<str:order_number>/', views.order_confirmation, name='confirmation'),
]
