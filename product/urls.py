from django.urls import path
from .views import CategoryList, CategoryDetail, ProductList, ReviewList, ReviewDetail, \
    ProductReviewsList, CategoryCreate, CategoryDetailUpdateDelete, ReviewCreate, ReviewDetailUpdateDelete, \
    ProductDetailUpdateDelete, ProductCreate, ProductDetail

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('reviews/', ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('products/reviews/', ProductReviewsList.as_view(), name='product-reviews-list'),
    path('categories/create/', CategoryCreate.as_view(), name='category-create'),
    path('categories/update/<int:pk>/', CategoryDetailUpdateDelete.as_view(), name='category-detail-update-delete'),
    path('products/create/', ProductCreate.as_view(), name='product-create'),
    path('products/update/<int:pk>/', ProductDetailUpdateDelete.as_view(), name='product-detail-update-delete')
    path('reviews/create/', ReviewCreate.as_view(), name='review-create'),
    path('reviews/update/<int:pk>/', ReviewDetailUpdateDelete.as_view(), name='review-detail-update-delete'),
]
