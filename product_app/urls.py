from django.urls import path
from . import views

urlpatterns = [
    path('fs/products/', views.get_fakestore_products, name='list_all_fakestore_products'),
    path('fs/products/<str:product_id>', views.get_fakestore_product_by_id, name='get_fakestore_product_by_id'),
    path('fs/products/categories/', views.get_fakestore_product_categories, name='get_all_fakestore_product_categories'),
    path('fs/products/category/<str:category>', views.get_fakestore_products_by_category, name='get_all_fakestore_products_by_category'),
    path('user/register/', views.register_user, name='register_user'),
    path('user/login/', views.login_user, name='login_user'),
    path('products/', views.get_products, name='get_all_products'),
    path('product/<str:product_id>/', views.get_product_by_id, name='get_product_by_id'),
    path('cart/', views.display_cart, name='display_cart'),
    path('cart/add/', views.add_to_cart, name='add_item_to_cart'),
]
