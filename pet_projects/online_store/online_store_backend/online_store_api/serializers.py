from rest_framework import serializers
from django.contrib.auth import get_user_model
from online_store_app.models import (
    Product, ProductSeller, ProductReview, SellerReview,
    Category,
    Cart, CartItem,
    Order, OrderItem,
)
from accountss.models import  Roles

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name_role')
    full_name = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['id','full_name', 'email', 'phone_number', 'roles']

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role_name = validated_data.pop('role')
        phone_number = validated_data.pop('phone_number', None)

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=phone_number,
        )

        role = Roles.objects.get(name_role=role_name)
        user.roles.add(role)

        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'parent',
            'is_active',
        ]

class ProductSerializer(serializers.ModelSerializer):
    max_discount = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'image_url',
            'category',
            'description',
            'rating',
            'rating_count',
            'quantity',
            'min_price',
            'max_price',
            'max_discount',
            'is_active',
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.images:
            return request.build_absolute_uri(obj.images.url)
        return None

    def get_max_discount(self, obj):
        offers = ProductSeller.objects.filter(product=obj)
        discount = [offer.discount for offer in offers if offer.discount]
        if not offers.exists():
            return None
        return max(discount) if discount else 0

    def get_min_price(self, obj):
        offers = ProductSeller.objects.filter(product=obj)
        min_price = [offer.final_price for offer in offers]
        if not offers.exists():
            return None
        return min(min_price) if min_price else 0

    def get_max_price(self, obj):
        offers = ProductSeller.objects.filter(product=obj)
        max_price = [offer.final_price for offer in offers]
        if not offers.exists():
            return None
        return max(max_price) if max_price else 0

class ProductSellerSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    seller = UserSerializer(read_only=True)
    seller_rating = serializers.CharField(source='seller.rating', read_only=True)
    seller_rating_count = serializers.IntegerField(source='seller.rating_count', read_only=True)
    old_price = serializers.SerializerMethodField()
    # discount_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductSeller
        fields = [
            'id',
            'product',
            'product_title',
            'seller',
            'seller_rating',
            'seller_rating_count',
            'price',
            'final_price',
            'old_price',
            'quantity',
            'discount',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'product', 'seller']

    def get_old_price(self, obj):
        if obj.discount:
            return obj.price
        return None

class CartItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'product_seller',
            'quantity',
        ]

class CartItemReadSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(
        source="product_seller.product.title",
        read_only=True
    )
    seller = serializers.CharField(
        source="product_seller.seller.email",
        read_only=True
    )
    price = serializers.DecimalField(
        source="price_at_time",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    old_price = serializers.SerializerMethodField()
    discount_percent = serializers.SerializerMethodField()
    total_price_product = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product_title',
            'product_seller',
            'seller',
            'price',
            'old_price',
            'discount_percent',
            'quantity',
            'total_price_product',
        ]
        read_only_fields = ['id']

    def get_total_price_product(self, obj):
        return obj.price_at_time * obj.quantity

    def get_old_price(self, obj):
        seller = obj.product_seller
        if seller.discount:
            return seller.price
        return None

    def get_discount_percent(self, obj):
        return obj.product_seller.discount or None

class CartSerializer(serializers.ModelSerializer):
    items = CartItemReadSerializer(many=True, read_only=True)
    total_price_cart = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = [
            'id',
            'items',
            'total_price_cart',
            'is_active',
        ]
        read_only_fields = ['id']

    def get_total_price_cart(self, obj):
        total_price = 0
        for item in obj.items.all():
            total_price += item.price_at_time * item.quantity

        return total_price

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'status',
            'total_price',
        ]

class OrderItemReadSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(
        source='product_seller.product.title',
        read_only=True
    )
    total_price_item = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'order',
            'product_title',
            'product_seller',
            'quantity',
            'price_at_time',
            'total_price_item',
        ]

    def get_total_price_item(self, obj):
        return obj.price_at_time * obj.quantity

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'total_price',
            'items',
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'order',
            'product_seller',
            'quantity',
            'price_at_time',
        ]

class ProductReviewSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # product = ProductSerializer(read_only=True)
    class Meta:
        model = ProductReview
        fields = [
            'id',
            'user',
            'product',
            'rating',
            'comment',
            'is_active',
        ]
        read_only_fields = ['id', 'user', 'product']

class SellerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerReview
        fields = [
            'id',
            'user',
            'seller',
            'rating',
            'comment',
            'is_active',
        ]
        read_only_fields = ['id', 'user', 'seller']