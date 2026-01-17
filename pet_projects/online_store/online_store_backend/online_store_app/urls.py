from django.urls import path
from online_store_app.views import (
    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,

    ProductSellerListView, ProductSellerCreateView, ProductSellerUpdateView, ProductSellerDeleteView,
    ProductSellerInProductListView,

    CartView, add_to_cart, increase_cart_item, decrease_cart_item, set_quantity,
    OrderCreateAndCreateOrderItemView, OrderListView, OrderDetailView,
    ProductReviewCreateView, ProductReviewUpdateView, ProductReviewDeleteView,
    SellerReviewCreateView, SellerReviewUpdateView, SellerReviewDeleteView,
)

app_name = 'online_store_app'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('product_detail/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product_create/', ProductCreateView.as_view(), name='product_create'),
    path('product_update/<int:product_id>/', ProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:product_id>/', ProductDeleteView.as_view(), name='product_delete'),

    path('product_seller_list/', ProductSellerListView.as_view(), name='product_seller_list'),
    path('product_seller_create/', ProductSellerCreateView.as_view(), name='product_seller_create'),
    path('product_seller_update/<int:product_seller_id>/', ProductSellerUpdateView.as_view(), name='product_seller_update'),
    path('product_seller_delete/<int:product_seller_id>/', ProductSellerDeleteView.as_view(), name='product_seller_delete'),
    path('product/<int:product_id>/offers/', ProductSellerInProductListView.as_view(), name='offers'),

    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_seller_id>/', add_to_cart, name='add_to_cart'),
    path('set_quantity/<int:cart_item_id>/', set_quantity, name='set_quantity'),
    path('increace/<int:cart_item_id>/', increase_cart_item, name='increase_cart_item'),
    path('decreace/<int:cart_item_id>/', decrease_cart_item, name='decrease_cart_item'),

    path('order_create/', OrderCreateAndCreateOrderItemView.as_view(), name='order_create'),
    path('order_list/', OrderListView.as_view(), name='order_list'),
    path('order_detail/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),

    path('product_review_create/<int:product_id>/', ProductReviewCreateView.as_view(), name='product_review_create'),
    path('product_review_update/<int:product_review_id>/', ProductReviewUpdateView.as_view(), name='product_review_update'),
    path('product_review_delete/<int:product_review_id>/', ProductReviewDeleteView.as_view(), name='product_review_delete'),

    path('seller_review_create/<int:seller_id>', SellerReviewCreateView.as_view(), name='seller_review_create'),
    path('seller_review_update/<int:seller_review_id>/', SellerReviewUpdateView.as_view(), name='seller_review_update'),
    path('seller_review_delete/<int:seller_review_id>/', SellerReviewDeleteView.as_view(), name='seller_review_delete'),
]