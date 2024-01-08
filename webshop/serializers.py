from rest_framework import serializers
from .models import Category, Stock, ProductReview, Product, UserInfo

class CategorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Category
        fields = '__all__'
    def validate_category_name(self, value): 
        if len(value) < 5: 
            raise serializers.ValidationError("Заголовок должен быть более 5 символов.") 
        return value 
    def validate_category_slug(self, value): 
        if len(value) < 5: 
            raise serializers.ValidationError("Заголовок должен быть более 5 символов.") 
        return value 

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ProductReview
        fields= '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = UserInfo
        fields = '__all__'
