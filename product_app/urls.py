from django.urls import path
from . import views

urlpatterns = [
    path('fs/products/', views.get_products, name='list_all_products'),
    path('fs/products/<str:product_id>', views.get_product_by_id, name='get_product_by_id'),
    path('fs/products/categories/', views.get_product_categories, name='get_all_product_categories'),
    path('fs/products/category/<str:category>', views.get_products_by_category, name='get_all_products_by_category')
]
