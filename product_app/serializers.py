from rest_framework import serializers
from django.db.models import Avg
from django.urls import reverse
from .models import User, Product, Category, Cart

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'phone_number', 'address']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def create(self, validated_data):
        # Use set_password to hash the password
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Use set_password to hash the password during update
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()  # To show category name
    ratings = serializers.SerializerMethodField()  # Custom field for rating details

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'ratings']

    def get_ratings(self, obj):
        """
        Custom method to calculate rating details.
        Args:
            obj (Product): The product instance.
        Returns:
            dict: Rating details with count and average rating.
        """
        ratings = obj.ratings.all()  # Fetch related ratings
        count = ratings.count()
        average = ratings.aggregate(average=Avg('rating'))['average']
        return {
            'count': count,
            'average': round(average, 2) if average else None
        }

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(source='products.count', read_only=True)
    products_link = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count', 'products_link']

    def get_products_link(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('get_products_by_category', args=[obj.id]))

class CartSerializer(serializers.ModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.id')
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['product_id', 'product_name', 'product_price', 'quantity', 'amount']
        extra_kwargs = {
            'user': {'write_only': True},
            'product': {'write_only': True},
            'quantity': {'required': True}
        }

    def get_amount(self, obj):
        return obj.quantity * obj.product.price

from rest_framework import serializers
from django.urls import reverse
from product_app.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items (only used when many=False)"""
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_name', 'quantity', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Orders (Supports both list and detailed views)"""
    order_id = serializers.UUIDField(source='id', read_only=True)
    order_placed_date = serializers.DateTimeField(source='created_at', format='%Y-%m-%d %H:%M:%S', read_only=True)
    item_count = serializers.IntegerField(source='items.count', read_only=True)
    order_link = serializers.SerializerMethodField()
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['order_id', 'item_count', 'total_amount', 'order_placed_date', 'order_link', 'order_items']

    def get_order_link(self, obj):
        """Generates link to order details page."""
        request = self.context.get('request')
        if self.context.get('many', False):
            return request.build_absolute_uri(reverse('get_order_by_id', args=[obj.id]))
        return None

    def get_order_items(self, obj):
        """Returns order items only when serializing a single order (many=False)."""
        if not self.context.get('many', False):
            return OrderItemSerializer(obj.items.all(), many=True).data
        return None
    
    def to_representation(self, instance):
        """Removes fields with None values"""
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value is not None}
