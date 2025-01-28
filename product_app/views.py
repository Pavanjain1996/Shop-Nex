import requests
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate

from .serializers import UserSerializer, ProductSerializer
from .models import User, Product
from .utils import generate_signed_token_for_user, token_required

FAKE_STORE_BASE_URL = "https://fakestoreapi.com"

def get_fakestore_products(request):
    products_url = f"{FAKE_STORE_BASE_URL}/products"

    try:
        response = requests.get(products_url)
        response.raise_for_status()
    except Exception as exc:
        return JsonResponse({
            "Message": f"Error connecting to fakestore service", 
            "Exception" : str(exc)
        }, safe=False, status=500)

    return JsonResponse(response.json(), safe=False, status=200)

def get_fakestore_product_by_id(request, product_id):
    product_url = f"{FAKE_STORE_BASE_URL}/products/{product_id}"

    try:
        response = requests.get(product_url)
        response.raise_for_status()
        if not response.content:
            raise Exception(f'Invalid product id {product_id}')
    except Exception as exc:
        return JsonResponse({
            "Message": f"Error connecting to fakestore service", 
            "Exception" : str(exc)
        }, safe=False, status=400)

    return JsonResponse(response.json(), safe=False, status=200)

def get_fakestore_product_categories(request):
    products_url = f"{FAKE_STORE_BASE_URL}/products/categories"

    try:
        response = requests.get(products_url)
        response.raise_for_status()
    except Exception as exc:
        return JsonResponse({
            "Message": f"Error connecting to fakestore service", 
            "Exception" : str(exc)
        }, safe=False, status=500)

    return JsonResponse(response.json(), safe=False, status=200)

def get_fakestore_products_by_category(request, category):
    products_url = f"{FAKE_STORE_BASE_URL}/products/category/{category}"

    try:
        response = requests.get(products_url)
        response.raise_for_status()
        if not response.json():
            return JsonResponse({
                "Message": "Invalid category", 
                "Exception" : f"No products for category : {category}"
            }, safe=False, status=404)
    except Exception as exc:
        return JsonResponse({
            "Message": f"Error connecting to fakestore service", 
            "Exception" : str(exc)
        }, safe=False, status=500)

    return JsonResponse(response.json(), safe=False, status=200)

@require_http_methods(["POST"])
@csrf_exempt
def register_user(request):
    data = json.loads(request.body)
    user_serializer = UserSerializer(data=data)
    if user_serializer.is_valid():
        created_user = user_serializer.save()
        return JsonResponse({
            'Message':  'User created successfully!', 
            'Username': created_user.email, 
            'Action': 'Please login to get the access token!'
        }, safe=False, status=200)
    else:
        return JsonResponse(user_serializer.errors, safe=False, status=400)

@require_http_methods(["POST"])
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
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

@token_required
def get_products(request):
    products = Product.objects.all()
    product_serializer = ProductSerializer(products, many=True)
    return JsonResponse({'Products': product_serializer.data}, safe=False, status=200)
