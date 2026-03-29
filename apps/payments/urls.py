from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('webhook/wompi/', views.wompi_webhook, name='wompi_webhook'),
]
