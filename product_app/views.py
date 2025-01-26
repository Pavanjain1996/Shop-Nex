import requests
import json
from django.http import JsonResponse

FAKE_STORE_BASE_URL = "https://fakestoreapi.com"

def get_products(request):
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

def get_product_by_id(request, product_id):
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
        }, safe=False, status=500)

    return JsonResponse(response.json(), safe=False, status=200)

def get_product_categories(request):
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

def get_products_by_category(request, category):
    products_url = f"{FAKE_STORE_BASE_URL}/products/category/{category}"

    try:
        response = requests.get(products_url)
        response.raise_for_status()
        if not response.json():
            return JsonResponse({
                "Message": "Invalid category", 
                "Exception" : f"No products for category : {category}"
            }, safe=False, status=400)
    except Exception as exc:
        return JsonResponse({
            "Message": f"Error connecting to fakestore service", 
            "Exception" : str(exc)
        }, safe=False, status=500)

    return JsonResponse(response.json(), safe=False, status=200)

