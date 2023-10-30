from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Count
from .models import Category, Product, Review, Tag
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ProductReviewsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        product_data = []
        for product in products:
            reviews = product.reviews.all()
            avg_rating = reviews.aggregate(Avg('stars'))['stars__avg']
            product_data.append({
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'category': product.category.name,
                'reviews': [review.text for review in reviews],
                'rating': avg_rating
            })
        return Response(product_data)

class CategoryCreate(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        tags = serializer.validated_data.get('tags', [])

        for tag in tags:
            if not Tag.objects.filter(name=tag.name).exists():
                # Если тэг не существует, создаем его
                Tag.objects.create(name=tag.name)

        product = serializer.save()
        product.tags.set(tags)  # Связываем тэги с товаром

class ProductDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ReviewCreate(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
