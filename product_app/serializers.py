from rest_framework import serializers
from django.db.models import Avg
from .models import User, Product

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
