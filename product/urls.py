# tweet/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결
    path('product/', views.product_list, name='product-list'), 
    path('product/create', views.product_create, name='product-create'),
    path('product/inbound', views.inbound_create, name='inbound'),
    path('product/outbound/', views.outbound_create, name='outbound'),     
    path('inventory/', views.inventory, name='inventory'),
    path('product/search', views.proudct_search, name='search-product')
]
