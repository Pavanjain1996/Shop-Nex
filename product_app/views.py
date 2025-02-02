import requests
import json
from uuid import UUID
from urllib.parse import urlencode

from django.http import JsonResponse, QueryDict
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate

from .serializers import UserSerializer, ProductSerializer, CartSerializer
from django.core.paginator import Paginator
from .models import User, Product, Cart, Order, OrderItem, Payment
from .authentication_utils import generate_signed_token_for_user, token_required
from .payment_utils import create_payment_link, verify_payment

PRODUCT_PAGE_SIZE = 10
MAX_ITEMS_ALLOWED = 500

@require_http_methods(["POST"])
@csrf_exempt
def register_user(request):
    data = json.loads(request.body or '{}')
    user_serializer = UserSerializer(data=data)
    if user_serializer.is_valid():
        created_user = user_serializer.save()
        return JsonResponse({
            'Message':  'User created successfully!', 
            'Username': created_user.email, 
            'Action': 'Please login to get the access token!'
        }, safe=False, status=201)
    else:
        return JsonResponse(user_serializer.errors, safe=False, status=400)

@require_http_methods(["POST"])
@csrf_exempt
def login_user(request):
    data = json.loads(request.body or '{}')
    username = data.get('username', '')
    password = data.get('password', '')
    if not username or not password:
        return JsonResponse({'Message': 'Username and Password are required fields.'}, safe=False, status=400)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'Message': 'Invalid Username!'}, safe=False, status=400)
    user = authenticate(username=username, password=password)
    if user is not None:
        return JsonResponse({
                'Message': 'Login successful!',
                'Username': user.username,
                'Token': generate_signed_token_for_user(user),
                "Expiry": "3600 seconds"
            },
            safe=False,
            status=200
        )
    else:
        return JsonResponse({'Message': 'Incorrect Password!'}, safe=False, status=401)

@require_http_methods(["GET"])
def get_products(request):
    page_number = int(request.GET.get('page', 1))
    if page_number < 1:
        return JsonResponse({'error': 'Invalid page number, it should be a positive number'}, status=400)
    
    page_size = min(int(request.GET.get('page_size', PRODUCT_PAGE_SIZE)), PRODUCT_PAGE_SIZE)

    products = Product.objects.all()
    paginator = Paginator(products, page_size)

    try:
        paginated_products = paginator.page(page_number)
    except:
        return JsonResponse({
            'error': 'Invalid page number',
            'total_pages': paginator.num_pages
        }, status=400)

    product_serializer = ProductSerializer(paginated_products, many=True)

    base_url = request.build_absolute_uri(reverse('get_all_products'))

    # Generate next and previous URLs
    next_url = f"{base_url}?{urlencode({'page': page_number + 1, 'page_size': page_size})}" if paginated_products.has_next() else None
    prev_url = f"{base_url}?{urlencode({'page': page_number - 1, 'page_size': page_size})}" if paginated_products.has_previous() else None

    response = {
        'total_products': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page_number,
        'products': product_serializer.data
    }
    if prev_url:
        response['previous'] = prev_url
    if next_url:
        response['next'] = next_url

    return JsonResponse(response, safe=False, status=200)

@require_http_methods(["GET"])
def get_product_by_id(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'Message': 'Invalid Product ID!'}, safe=False, status=400)
    
    product_serializer = ProductSerializer(product)

    return JsonResponse(product_serializer.data, safe=False, status=200)

@require_http_methods(["GET"])
@token_required
def display_cart(request):
    cart_items = Cart.objects.filter(user=request.user_data['user_id'])
    if not cart_items:
        return JsonResponse({"Message": "Cart is empty!"}, safe=False, status=200)

    serializer = CartSerializer(cart_items, many=True)
    
    total_amount = sum(item['amount'] for item in serializer.data)

    return JsonResponse({
        "cart_items": serializer.data,
        "total_cart_amount": total_amount
    }, safe=False, status=200)

@require_http_methods(["POST"])
@csrf_exempt
@token_required
def add_to_cart(request):
    data = json.loads(request.body or '{}')
    product_id = data.get('product_id')
    if not product_id:
        return JsonResponse({"Message": "Missing product id!"}, safe=False, status=400)
    quantity = data.get('quantity')
    if not quantity:
        return JsonResponse({"Message": "Missing quantity for the product!"}, safe=False, status=400)
    try:
        quantity = int(quantity)
        if quantity < 1:
            return JsonResponse({"Message": "Invalid quantity!"}, safe=False, status=400)
        if quantity > MAX_ITEMS_ALLOWED:
            return JsonResponse({"Message": "Maximum quantity allowed is 500!"}, safe=False, status=400)
    except Exception:
        return JsonResponse({"Message": "Invalid quantity!"}, safe=False, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"Message": "Invalid product ID!"}, safe=False, status=400)
    
    cart = Cart.objects.filter(
        user=User.objects.get(id=request.user_data['user_id']),
        product=product
    )
    if cart and cart[0]:
        total_quantity = cart[0].quantity + quantity
        if total_quantity > MAX_ITEMS_ALLOWED:
            return JsonResponse({
                "Message": "Maximum quantity allowed is 500!",
                "Current Quantity": cart[0].quantity
            }, safe=False, status=400)
        cart[0].quantity = total_quantity
        cart[0].save()
        return JsonResponse({
            "Message": "Product already present in the cart",
            "product": product.name,
            "quantity_added": quantity,
            'total_quantity': total_quantity
        }, safe=False, status=201)
    else:
        Cart.objects.create(
            user=User.objects.get(id=request.user_data['user_id']),
            product=product,
            quantity=quantity
        )
        return JsonResponse({
            "Message": "Product added to cart",
            "product": product.name,
            "quantity": quantity
        }, safe=False, status=201)

@require_http_methods(["POST"])
@csrf_exempt
@token_required
def remove_from_cart(request):
    data = json.loads(request.body or '{}')
    product_id = data.get('product_id')
    if not product_id:
        return JsonResponse({"Message": "Missing product id!"}, safe=False, status=400)
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"Message": "Invalid product ID!"}, safe=False, status=400)
    cart = Cart.objects.filter(
        user=User.objects.get(id=request.user_data['user_id']),
        product=product
    )
    if cart and cart[0]:
        quantity = data.get('quantity')
        if not quantity:
            cart[0].delete()
            return JsonResponse({"Message": f"{product.name} is removed from your cart!",}, safe=False, status=400)
        else:
            try:
                quantity = int(quantity)
                if quantity < 1:
                    return JsonResponse({"Message": "Invalid quantity!"}, safe=False, status=400)
            except Exception:
                return JsonResponse({"Message": "Invalid quantity!"}, safe=False, status=400)
            if quantity > cart[0].quantity:
                return JsonResponse({"Message": f"{quantity} quantity of {product.name} is not available in your cart!"}, safe=False, status=400)

        total_quantity = cart[0].quantity - quantity
        if total_quantity == 0:
            cart[0].delete()
            return JsonResponse({"Message": f"{product.name} is removed from your cart!",}, safe=False, status=201)
        else:
            cart[0].quantity = total_quantity
            cart[0].save()
            return JsonResponse({
                "Message": f"{quantity} quantity of {product.name} have been removed from your cart!",
                "product": product.name,
                'total_quantity': total_quantity
            }, safe=False, status=201)
    else:
        return JsonResponse({
            "Message": "This product is not present in your cart",
            "product": product.name,
        }, safe=False, status=200)

@require_http_methods(["GET"])
@token_required
def checkout_from_cart(request):
    user = User.objects.get(id=request.user_data['user_id'])
    cart_items =  Cart.objects.filter(user=user)
    if not cart_items:
        return JsonResponse({"Message": "Cart is empty!"}, safe=False, status=200)

    # Create an empty order
    order = Order.objects.create(user=user, total_amount=0)

    # Create order items from each cart item
    total_amount = 0
    for cart_item in cart_items:
        amount = cart_item.product.price*cart_item.quantity
        order_item = OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            amount=amount
        )
        total_amount += amount
    
    # Update amount for the order
    order.total_amount = total_amount
    order.save()

    # Empty cart once order is created
    Cart.objects.filter(user=user).delete()

    # Generate payment link
    payment_meta = create_payment_link(order)
    payment_id = payment_meta.get('id')
    payment_link = payment_meta.get('short_url')
    payment = Payment.objects.create(
        id=payment_id,
        order=order,
        payment_link=payment_link
    )

    return JsonResponse({
        "Message": "Your order has been created, please use the given payment link and complete the payment!",
        "Order ID": str(order.id),
        "Payment Link": payment_link
    }, safe=False, status=201)

@require_http_methods(["GET"])
def payment_callback(request):
    payment = {
        'payment_link_id': request.GET['razorpay_payment_link_id'],
        'payment_link_reference_id': request.GET['razorpay_payment_link_reference_id'],
        'payment_link_status': request.GET['razorpay_payment_link_status'],
        'razorpay_payment_id': request.GET['razorpay_payment_id'],
        'razorpay_signature': request.GET['razorpay_signature']
    }
    verified = verify_payment(payment)
    if not verified:
        JsonResponse({
            "Message": "Unverified Request!"
        }, safe=False, status=401)

    payment_obj = Payment.objects.get(id=request.GET['razorpay_payment_link_id'])
    payment_obj.status = 'SUCCESS'
    payment_obj.save()

    order = Order.objects.get(id=payment_obj.order.id)
    order.status = "PROCESSING"
    order.save()

    params = QueryDict(mutable=True)
    params['order_id'] = str(order.id)
    path = reverse('completed_order')
    return redirect(f'{path}?{params.urlencode()}')

@require_http_methods(["GET"])
def order_completed(request):
    return JsonResponse({
        "Message": "Your order is accepted!",
        "Order reference id": str(request.GET['order_id'])
    }, safe=False, status=200)

@require_http_methods(["POST"])
@csrf_exempt
@token_required
def order_status(request):
    data = json.loads(request.body or '{}')
    order_id = data.get('order_id')
    print(data)
    if not order_id:
        return JsonResponse({"Message": "Missing order id!"}, safe=False, status=400)
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({"Message": "Invalid order id!"}, safe=False, status=400)
    
    return JsonResponse({
        "Message": "Status for your order!",
        "Order ID": str(order.id),
        "Status": order.status
    }, safe=False, status=200)

@require_http_methods(["POST"])
@csrf_exempt
@token_required
def order_cancel(request):
    data = json.loads(request.body or '{}')
    order_id = data.get('order_id')
    print(data)
    if not order_id:
        return JsonResponse({"Message": "Missing order id!"}, safe=False, status=400)
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({"Message": "Invalid order id!"}, safe=False, status=400)
    
    order.status = "CANCELLED"
    order.save()

    return JsonResponse({
        "Message": "Status for your order!",
        "Order ID": str(order.id),
        "Status": order.status
    }, safe=False, status=200)
