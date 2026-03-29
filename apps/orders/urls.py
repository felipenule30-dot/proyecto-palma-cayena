from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('seguimiento/', views.order_tracking, name='tracking'),
]
