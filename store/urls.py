from django.urls import path
from . import views
from .views import (
    ProductCreateView, ProductListView, ProductDetailView, ProductUpdateView, ProductDeleteView,ProductSearch,
    CategoryCreateView, CategoryListView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView,
    ReviewCreateView, ReviewListView, ReviewDetailView, ReviewUpdateView, ReviewDeleteView,SellerListCreateView,SellerRetrieveUpdateDestroyView,SellerOrderView, CartView, AddToCartView,UpdateCartItem,DeleteCartItem
)


urlpatterns = [
    # PRODUCT ENDPOINTS
    path('api/products/', ProductListView.as_view(), name='product-list'),
    path('api/products/create/', ProductCreateView.as_view(), name='product-create'),
    path('api/products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('api/products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('api/products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('api/search/', ProductSearch.as_view(), name='search'),

    # PRODUCT REVIEW ENDPOINTS
    path('api/reviews/', ReviewCreateView.as_view(), name='review-create'),
    path('api/reviews/<int:product_id>/', ReviewListView.as_view(), name='review-list'),
    path('api/reviews/detail/<int:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
    path('api/reviews/update/<int:review_id>/', ReviewUpdateView.as_view(), name='review-update'),
    path('api/reviews/delete/<int:review_id>/', ReviewDeleteView.as_view(), name='review-delete'),

    # CATEGORY ENDPOINTS
    path('api/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('api/categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('api/categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('api/categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    # SELLER ENDPOINTS
    path('api/sellers/', SellerListCreateView.as_view(), name='seller-list-create'),
    path('api/sellers/<int:pk>/', SellerRetrieveUpdateDestroyView.as_view(), name='seller-retrieve-update-destroy'),
    path('api/seller_orders/', SellerOrderView.as_view(), name='seller_orders'),

    # CART ENDPOINTS
    path('api/cart/', CartView.as_view(), name='cart-view'),
    path('api/add_to_cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('api/update_cart_item/<str:pk>/', UpdateCartItem.as_view(), name='update_cart_item'),
    path('api/delete_cart_item/<str:pk>/', DeleteCartItem.as_view(), name='delete_cart_item'),
]
