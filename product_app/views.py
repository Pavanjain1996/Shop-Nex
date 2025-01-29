import requests
import json
from urllib.parse import urlencode

from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate

from .serializers import UserSerializer, ProductSerializer
from django.core.paginator import Paginator
from .models import User, Product
from .utils import generate_signed_token_for_user, token_required

FAKE_STORE_BASE_URL = "https://fakestoreapi.com"
PRODUCT_PAGE_SIZE = 10

@require_http_methods(["GET"])
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

@require_http_methods(["GET"])
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

@require_http_methods(["GET"])
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

@require_http_methods(["GET"])
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
        }, safe=False, status=201)
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

@require_http_methods(["GET"])
@token_required
def get_products(request):
    page_number = int(request.GET.get('page', 1))
    if page_number < 1:
        return JsonResponse({'error': 'Invalid page number, it should be a positive number',}, status=400)
    
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
@token_required
def get_product_by_id(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'Message': 'Invalid Product ID!'}, safe=False, status=400)
    
    product_serializer = ProductSerializer(product)

    return JsonResponse(product_serializer.data, safe=False, status=200)
