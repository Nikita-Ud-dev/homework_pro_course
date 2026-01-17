import jwt
from django.conf import settings
from django.core.exceptions import ValidationError, PermissionDenied
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from accountss.models import OnlineStoreUser, Roles
from online_store_app.models import (
    Product, ProductSeller, ProductReview, SellerReview,
    Cart, CartItem,
    Order, OrderItem,
)

from online_store_api.serializers import (
    UserSerializer, RegisterSerializer,
    ProductSerializer,
    ProductSellerSerializer,
    CartSerializer,
    CartItemReadSerializer, CartItemWriteSerializer,
    OrderSerializer, OrderDetailSerializer,
    ProductReviewSerializer,
    SellerReviewSerializer,
)

from online_store_api.permissions import (
    IsProductSellerOrAdminOwner, IsCartOrAdminOwner, IsReviewAuthorOrAdmin, IsOrderOrAdminOwner,
    IsSellerOrAdmin, IsBuyerOrAdmin, IsAdmin,
)

# Create your views here.

User = get_user_model()

class OnlineStoreUserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='become-buyer')
    def become_buyer(self, request):
        user = request.user

        if user.roles.filter(name_role='buyer').exists():
            return Response({'detail': 'Already buyer'})

        buyer_role = Roles.objects.get(name_role='buyer')
        user.roles.add(buyer_role)

        return Response({'detail': 'User become buyer'})

    @action(detail=False, methods=['post'], url_path='become-seller')
    def become_seller(self, request):
        user = request.user

        if user.roles.filter(name_role='seller').exists():
            return Response({'detail': 'Already seller'})

        seller_role = Roles.objects.get(name_role='seller')
        user.roles.add(seller_role)

        return Response({'detail': 'User become seller'})

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'User created'}, status=status.HTTP_201_CREATED)

class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        products = list(Product.objects.filter(is_active=True))

        bought_product_ids = OrderItem.objects.filter(
            order__user=user,
            order__status='paid'
        ).values_list('product_seller__product_id', flat=True)

        bought_product_ids = set(bought_product_ids)

        products.sort(
            key=lambda product: (
                product.id not in bought_product_ids,
                product.id
            )
        )

        serializer = ProductSerializer(
            products,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


class ProductReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsAuthenticated(), IsAdmin()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsAdmin()]
        return super().get_permissions()

class ProductSellerReadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductSeller.objects.all()
    serializer_class = ProductSellerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        # for offer in queryset:
        #     if offer.quantity > 0:
        #         offer.is_active = True

        return queryset

class ProductSellerViewSet(viewsets.ModelViewSet):
    queryset = ProductSeller.objects.all()
    serializer_class = ProductSellerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        product_id = self.request.query_params.get('product_id')

        if user.roles.filter(name_role__in=['seller', 'admin']).exists() and product_id:
            queryset = queryset.filter(seller=user, product_id=product_id)

        return queryset


    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsAuthenticated(), IsSellerOrAdmin()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsSellerOrAdmin(), IsProductSellerOrAdminOwner()]
        return super().get_permissions()

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')

        if not product_id:
            raise ValidationError({'product': 'Product ID is required'})

        product = get_object_or_404(Product, id=product_id)

        serializer.save(
            seller=self.request.user,
            product=product,
        )

    def update(self, request, *args, **kwargs):
        offer = self.get_object()

        if offer.quantity > 0:
            offer.is_active = True
            offer.save()

        return super().update(request, *args, **kwargs)

class CartViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsBuyerOrAdmin]

    def list(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CartItemViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return CartItemReadSerializer
        return CartItemWriteSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'create'):
            return [IsAuthenticated(), IsBuyerOrAdmin()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsBuyerOrAdmin(), IsCartOrAdminOwner()]
        return super().get_permissions()

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user, is_active=True)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        user = self.request.user

        # if not user.roles.name_role == 'buyer':
        #     raise PermissionDenied('USER_IS_NOT_BUYER')

        cart, _ = Cart.objects.get_or_create(user=self.request.user, is_active=True)
        product_seller = serializer.validated_data['product_seller']
        cart_item = CartItem.objects.filter(cart=cart, product_seller=product_seller).first()

        if not cart_item:
            serializer.save(cart=cart, price_at_time=product_seller.final_price, quantity=1)
        else:
            cart_item.quantity += 1
            cart_item.save()


    def update(self, request, *args, **kwargs):
        item = self.get_object()
        new_quantity = request.data.get('quantity')
        if not new_quantity:
            return Response({'error': 'Поле "quantity" є обов`язковим'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_quantity = int(new_quantity)
        except ValueError:
            return Response({'error': '"quantity" повинно бути числом'}, status=status.HTTP_400_BAD_REQUEST)

        if new_quantity <= 0:
            return Response({'error': 'Кількість продукту повинна бути більше нуля'},
                            status=status.HTTP_400_BAD_REQUEST)
        if new_quantity > item.product_seller.quantity:
            return Response({'error': 'Кількість продукту не бути більше чім є в наявності'},
                            status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            return Response({'message': 'Кількість зменшено'}, status=status.HTTP_200_OK)

        else:
            return super().destroy(request, *args, **kwargs)

class OrderViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'create'):
            return [IsAuthenticated(), IsBuyerOrAdmin()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsOrderOrAdminOwner()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        user = self.request.user
        cart = Cart.objects.get(user=user, is_active=True)

        if not cart or not cart.items.exists():
            raise ValidationError('Кошик порожній')

        order = serializer.save(user=user, status='created', total_price=cart.get_total_price_cart())

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product_seller=item.product_seller,
                quantity=item.quantity,
                price_at_time=item.price_at_time,
            )
        cart.is_active = False
        cart.save()

    @transaction.atomic
    def handle_payment(self, order):
        for item in order.items.all():
            product_seller = item.product_seller
            if item.quantity > item.product_seller.quantity:
                raise ValidationError('Недостатьно товару')

            product_seller.quantity -= item.quantity

            if product_seller.quantity == 0:
                product_seller.quantity = 0
                product_seller.is_active = False
            product_seller.save()

        order.status = 'paid'
        order.save()

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def pay(self, request, pk=None):
        order = self.get_object()

        if order.status != 'created':
            return Response(
                {'error': 'Замовлення вже оброблено'},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.handle_payment(order)

        return Response(
            {'detail': 'Оплата успішна'},
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        return Response(
            {'error': 'Зміна замовлення заборонена'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class ProductReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]


class MyProductReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReviewSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'create'):
            return [IsAuthenticated(), IsBuyerOrAdmin()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsBuyerOrAdmin(), IsReviewAuthorOrAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        return ProductReview.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')

        if not product_id:
            raise ValidationError({'product': 'Product ID is required'})

        product = get_object_or_404(Product, id=product_id)

        serializer.save(
            user=self.request.user,
            product=product,
        )

class SellerReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SellerReview.objects.all()
    serializer_class = SellerReviewSerializer
    permission_classes = [IsAuthenticated]


class MySellerReviewViewSet(viewsets.ModelViewSet):
    serializer_class = SellerReviewSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'create'):
            return [IsAuthenticated(), IsBuyerOrAdmin()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsBuyerOrAdmin(), IsReviewAuthorOrAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        return SellerReview.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        seller_id = self.request.data.get('seller')

        if not seller_id:
            raise ValidationError({'seller': 'Seller ID is required'})

        seller = get_object_or_404(OnlineStoreUser, id=seller_id)

        serializer.save(
            user=self.request.user,
            seller=seller
        )


# class OnlineStoreTokenObtainPair(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(username=email, password=password)
#         if user:
#             tokens = generate_jwt_token(user)
#             return Response(tokens, status=status.HTTP_200_OK)
#         return Response({'error': 'Недійсні дані для авторизації'}, status=status.HTTP_401_UNAUTHORIZED)
#
# class OnlineStoreTokenRefreshPair(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         refresh_token = request.data.get('refresh')
#         try:
#             payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
#             user_id = payload['user_id']
#             user = User.objects.get(id=user_id)
#             tokens = generate_jwt_token(user)
#             return Response(tokens, status=status.HTTP_200_OK)
#         except jwt.ExpiredSignatureError:
#             return Response({'error': 'Недійсний токен'}, status=status.HTTP_401_UNAUTHORIZED)
#         except jwt.InvalidTokenError:
#             return Response({'error': 'Недійсний токен'}, status=status.HTTP_401_UNAUTHORIZED)
#         except User.DoesNotExist:
#             return Response({'error': 'Недійсний користувач'}, status=status.HTTP_401_UNAUTHORIZED)
