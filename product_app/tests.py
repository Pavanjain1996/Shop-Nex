from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
import requests

class ProductAPITests(TestCase):

    @patch('requests.get')
    def test_list_all_products(self, mock_get):
        # Mock response data from FakeStoreAPI
        mock_response = [
            {'id': 1, 'title': 'Product 1', 'price': 10.99},
            {'id': 2, 'title': 'Product 2', 'price': 15.99},
        ]
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        # Test the list all products API endpoint
        response = self.client.get(reverse('list_all_fakestore_products'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_response)
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Product 2')

    @patch('requests.get')
    def test_get_product_by_id(self, mock_get):
        product_id = 1
        mock_response = {'id': 1, 'title': 'Product 1', 'price': 10.99}
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        # Test the get product by ID API
        response = self.client.get(reverse('get_fakestore_product_by_id', args=[product_id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_response)

    @patch('requests.get')
    def test_list_categories(self, mock_get):
        mock_response = ['electronics', 'clothing', 'jewelery']
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        # Test the list categories API
        response = self.client.get(reverse('get_all_fakestore_product_categories'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_response)

    @patch('requests.get')  # Mocking requests.get
    def test_get_products_by_category(self, mock_get):
        category = 'electronics'
        mock_response = [
            {'id': 1, 'title': 'Product 1', 'category': 'electronics'},
            {'id': 2, 'title': 'Product 2', 'category': 'electronics'}
        ]
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        # Test the get products by category API
        response = self.client.get(reverse('get_all_fakestore_products_by_category', args=[category]))
        print(response.status_code)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_response)
