from django.urls import path
from . import views
from .views import (
    ProductCreateView, ProductListView, ProductDetailView, ProductUpdateView, ProductDeleteView,ProductSearch,
    CategoryCreateView, CategoryListView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView,
    ReviewCreateView, ReviewListView, ReviewDetailView, ReviewUpdateView, ReviewDeleteView,SellerListCreateView,SellerRetrieveUpdateDestroyView,OrdersView,OrderDetailView, AdminOrderUpdateDeleteView,CartView, AddToCartView,UpdateCartItem,DeleteCartItem, AdminUpdateDeleteCartItem,PromotionListCreateAPIView,PromotionRetrieveUpdateDestroyAPIView,ProductListCreateAPIView,ProductRetrieveUpdateDestroyAPIView,SellerOrdersAPIView,UserProfileView,BillingAddressListCreateAPIView,BillingAddressRetrieveUpdateDestroyAPIView,AdminUserBillingAddressesAPIView,AdminBillingAddressDetailAPIView

)


urlpatterns = [
    #USER ENDPOINT
    path('api/billing-addresses/', BillingAddressListCreateAPIView.as_view(), name='billing-address-list-create'),
    path('api/billing-addresses/<int:pk>/', BillingAddressRetrieveUpdateDestroyAPIView.as_view(), name='billing-address-retrieve-update-destroy'),


    # PRODUCT ENDPOINTS
    path('api/products/', ProductListView.as_view(), name='product-list'),
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
    path('api/products/create/', ProductCreateView.as_view(), name='product-create'),
    path('api/seller/orders/', SellerOrdersAPIView.as_view(), name='seller-orders'),
    
    
    # CART ENDPOINTS
    path('api/cart/', CartView.as_view(), name='cart-view'),
    path('api/add_to_cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('api/update_cart_item/<str:pk>/', UpdateCartItem.as_view(), name='update_cart_item'),
    path('api/delete_cart_item/<str:pk>/', DeleteCartItem.as_view(), name='delete_cart_item'),


    #ADMIN ENDPOINTS
    path('api/admin/orders/', OrdersView.as_view(), name='orders'),
    path('api/admin/order_detail/<str:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('api/admin/order_update_delete/<str:pk>', AdminOrderUpdateDeleteView.as_view(), name='order_update_delete'),
    path('api/admin/order/<str:cart_pk>/item/<str:pk>/', AdminUpdateDeleteCartItem.as_view(), name='admin_update_delete_cart_item'),
    path('api/admin/promotions/', PromotionListCreateAPIView.as_view(), name='promotion-list-create'),
    path('api/admin/promotions/<int:pk>/', PromotionRetrieveUpdateDestroyAPIView.as_view(), name='promotion-retrieve-update-destroy'),
    path('api/admin/products/', ProductListCreateAPIView.as_view(), name='admin-product-list-create'),
    path('api/admin/products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='admin-product-retrieve-update-destroy'),
    path('api/admin/sellers/', SellerListCreateView.as_view(), name='seller-list-create'),
    path('api/admin/sellers/<int:pk>/', SellerRetrieveUpdateDestroyView.as_view(), name='seller-retrieve-update-destroy'),
    path('api/user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/admin/<int:user_id>/billing-addresses/', AdminUserBillingAddressesAPIView.as_view(), name='admin-user-billing-addresses'),
    path('api/admin/billing-addresses/<int:pk>/', AdminBillingAddressDetailAPIView.as_view(), name='admin-billing-address-detail'),

    
    
    
    
    
    
    
    ]
