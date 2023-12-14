User Management:
User Registration:

POST /api/register/
User Authentication:

POST /api/login/
POST /api/logout/
User Profile:

GET /api/user/profile/
PUT /api/user/profile/


Product Management:
Product Listing:

GET /api/products/
Product Detail:

GET /api/products/{product_id}/
Product Creation:

POST /api/products/
Product Update:

PUT /api/products/{product_id}/
Product Deletion:

DELETE /api/products/{product_id}/





Seller Management:
Seller Profile:

GET /api/sellers/{seller_id}/
Seller Products:

GET /api/sellers/{seller_id}/products/
Order Management:
Cart Operations:

GET /api/cart/
POST /api/cart/add/
PUT /api/cart/update/
DELETE /api/cart/remove/



Checkout:

POST /api/checkout/
Order History:

GET /api/orders/
GET /api/orders/{order_id}/
Reviews and Ratings:
Product Reviews:
GET /api/products/{product_id}/reviews/
POST /api/products/{product_id}/reviews/
Search and Filtering:
Product Search:
GET /api/products/search/?query={search_query}
GET /api/products/filter/?category={category}&price_range={range}
Miscellaneous:
Categories:

GET /api/categories/
Featured Products:

GET /api/featured-products/
Promotions/Discounts:

GET /api/promotions/
GET /api/products/{product_id}/promotions/
Seller Dashboard:
Seller Dashboard Stats:

GET /api/seller/dashboard/
Seller Orders:

GET /api/seller/orders/
GET /api/seller/orders/{order_id}/
Integration with Payment Gateway:
Payment Processing:
POST /api/payment/
Notifications:
User Notifications:
GET /api/notifications/
PUT /api/notifications/mark-as-read/
Authentication and Authorization:
Token Refresh:

POST /api/token/refresh/
Token Revoke:

POST /api/token/revoke/
Admin (for platform administrators):
Admin Dashboard:

GET /api/admin/dashboard/
Admin Product Management:

GET /api/admin/products/
PUT /api/admin/products/{product_id}/
Admin Order Management:

GET /api/admin/orders/
PUT /api/admin/orders/{order_id}/
Admin User Management:

GET /api/admin/users/
PUT /api/admin/users/{user_id}/