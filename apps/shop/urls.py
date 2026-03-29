from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.shop_list, name='list'),
    path('categoria/<slug:slug>/', views.category_detail, name='category'),
    path('coleccion/<slug:slug>/', views.collection_detail, name='collection'),
    path('producto/<slug:slug>/', views.product_detail, name='product_detail'),
]
