from django.urls import path
from . import views

urlpatterns = [
    path('user/register/', views.register_user, name='register_user'),
    path('user/login/', views.login_user, name='login_user'),
    path('products/', views.get_products, name='get_all_products'),
    path('product/<str:product_id>/', views.get_product_by_id, name='get_product_by_id'),
    path('cart/', views.display_cart, name='display_cart'),
    path('cart/add/', views.add_to_cart, name='add_item_to_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_item_from_cart'),
    path('cart/checkout/', views.checkout_from_cart, name='checkout_from_cart'),
    path('payment/callback/', views.payment_callback, name="callback_url_for_payment"),
    path('order/completed/', views.order_completed, name='completed_order')
]
