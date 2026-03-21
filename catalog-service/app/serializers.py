from rest_framework import serializers
from .models import Category, Tag, BookCategory, BookTag, CatalogSearchHistory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = '__all__'

class BookTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTag
        fields = '__all__'

class CatalogSearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogSearchHistory
        fields = '__all__'
