from django.urls import path
from .views import (
    ProductCreateView, ProductListView, ProductDetailView, ProductUpdateView, ProductDeleteView,
    CategoryCreateView, CategoryListView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView,
    ReviewCreateView, ReviewListView, ReviewDetailView, ReviewUpdateView, ReviewDeleteView,SellerListCreateView,SellerRetrieveUpdateDestroyView
)







urlpatterns = [
    #PRODUCT ENDPOINTS
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    #PRODUCT REVIEW ENDPOINTS
    path('reviews/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:product_id>/', ReviewListView.as_view(), name='review-list'),
    path('reviews/detail/<int:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/update/<int:review_id>/', ReviewUpdateView.as_view(), name='review-update'),
    path('reviews/delete/<int:review_id>/', ReviewDeleteView.as_view(), name='review-delete'),


    #CATEGORY ENDPOINTS
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    #SELLER ENDPOINTS
    path('sellers/', SellerListCreateView.as_view(), name='seller-list-create'),
    path('sellers/<int:pk>/', SellerRetrieveUpdateDestroyView.as_view(), name='seller-retrieve-update-destroy'),
    # Add more paths as needed
]
