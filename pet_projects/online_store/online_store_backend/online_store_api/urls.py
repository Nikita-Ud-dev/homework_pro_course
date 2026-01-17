from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from online_store_api.views import RegisterView, RecommendationView
from online_store_api.views import (
    OnlineStoreUserViewSet,
    ProductViewSet, ProductReadOnlyViewSet, ProductSellerViewSet,ProductSellerReadViewSet,
    CartViewSet, CartItemViewSet,
    OrderViewSet,
    ProductReviewViewSet, MyProductReviewViewSet,
    SellerReviewViewSet, MySellerReviewViewSet,
)

router = DefaultRouter()
router.register(r'users', OnlineStoreUserViewSet, basename='users')
router.register(r'products', ProductViewSet)
router.register(r'products-catalog', ProductReadOnlyViewSet, basename='products-catalog')
router.register(r'product-offers', ProductSellerViewSet)
router.register(r'product-offers-catalog', ProductSellerReadViewSet, basename='product-offers-catalog')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cart_items')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'product-reviews', ProductReviewViewSet)
router.register(r'my-product-reviews', MyProductReviewViewSet, basename='my_product_reviews')
router.register(r'seller-reviews', SellerReviewViewSet)
router.register(r'my-seller-reviews', MySellerReviewViewSet, basename='my_seller_reviews')


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('recommendations/', RecommendationView.as_view(), name='recommendations'),
]