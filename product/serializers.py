# product/serializers.py
from rest_framework import serializers
from .models import Category, Product, Review, Tag


class CategorySerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='name',
        allow_empty=False,
    )
    class Meta:
        model = Category
        fields = ['title', 'description', 'price', 'category', 'tags']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']

        @staticmethod
        def validate_tags(value):
            for tag in value:
                if not Tag.objects.filter(name=tag.name).exists():
                    raise serializers.ValidationError(f"Тэг '{tag.name}' не существует в базе данных.")
            return value

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']

