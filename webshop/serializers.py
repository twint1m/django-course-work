from rest_framework import serializers
from .models import Category, Stock, ProductReview

class CategorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Category
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ProductReview
        fields= '__all__'
