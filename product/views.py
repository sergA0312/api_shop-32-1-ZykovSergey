from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Count
from .models import Category, Product, Review, Tag
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer

# Вьюшка для списка категорий и их создания
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Вьюшка для деталей категории, обновления и удаления
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Вьюшка для списка продуктов и их создания
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Вьюшка для деталей продукта, обновления и удаления
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Вьюшка для списка отзывов и их создания
class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Вьюшка для деталей отзыва, обновления и удаления
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Вьюшка для списка отзывов по продукту
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

# Вьюшка для создания категории
class CategoryCreate(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Вьюшка для деталей категории, обновления и удаления
class CategoryDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Вьюшка для создания продукта
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

# Вьюшка для деталей продукта, обновления и удаления
class ProductDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Вьюшка для создания отзыва
class ReviewCreate(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Вьюшка для деталей отзыва, обновления и удаления
class ReviewDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
