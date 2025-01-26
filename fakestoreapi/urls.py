from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_products, name='list_all_products'),
    path('products/<str:product_id>', views.get_product_by_id, name='get_product_by_id'),
]
