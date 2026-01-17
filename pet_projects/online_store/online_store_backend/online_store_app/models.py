from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
# Create your models here.

User = get_user_model()

class Product(models.Model):
    title = models.CharField(max_length=30, verbose_name='Назва продукту')
    description = models.TextField(max_length=500, blank=False, verbose_name='Опис продукту')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення продукту')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення продукту')
    sellers = models.ManyToManyField(
        User,
        through='online_store_app.ProductSeller',
        related_name='products',
        verbose_name='Продавці які пропонують продукт'
    )
    category = models.ForeignKey(
    'online_store_app.Category',
        on_delete=models.SET_NULL,
        null=True, blank=False,
        related_name='products',
        verbose_name='Категірії продуктів'
    )
    quantity = models.IntegerField(null=True, blank=True, verbose_name='Кільксть продуктів на ринку')
    is_active = models.BooleanField(default=True, verbose_name='Статус наявності продукту')
    images = models.ImageField(
        upload_to='product_images/',
        null=True, blank=True,
        verbose_name='Фотографії продукту'
    )
    rating = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True, blank=True,
        verbose_name='Середня оцінка рейтинга продукту'
    )
    rating_count = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name='Кількість відгуків'
    )

    def __str__(self):
        return f'{self.title} -- {self.category} -- {self.quantity} -- {self.rating} -- {self.is_active}'

class ProductSeller(models.Model):
    product = models.ForeignKey(
        'online_store_app.Product',
        on_delete=models.CASCADE,
        null= False, blank=False,
        related_name = 'product_sellers',
        verbose_name='Вибранний продукт'
    )
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Продавець')
    price = models.PositiveIntegerField(
        validators=[MaxValueValidator(10000000)],
        blank=False, verbose_name='Ціна продукту'
    )
    final_price = models.IntegerField(
        default=0,
        verbose_name='Фінальна ціна продукту',
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50000)],
        null=False, blank=False,
        verbose_name='Кількість продуктів у продавця'
    )
    discount = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, blank=True,
        verbose_name='Знижка на продукт'
    )
    is_active = models.BooleanField(default=True, null=True, blank=True, verbose_name='Наявність продукту')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення ціни на продукт')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення ціни на продукт')

    def save(self, *args, **kwargs):
        if self.discount:
            self.final_price = self.price * (100 - self.discount) / 100
        else:
            self.final_price = self.price

        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('product', 'seller')

    def __str__(self):
        return f'{self.product} -- {self.seller} -- {self.price} -- {self.quantity} -- {self.is_active}'

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Назва категорії')
    slug = models.SlugField(unique=True, verbose_name='Назва слагу')
    is_active = models.BooleanField(default=True, verbose_name='Статус категорії')
    parent = models.ForeignKey(
        'online_store_app.Category', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='children',
        verbose_name='Вибір основної категорії '
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення категорії')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення категорії')

    def __str__(self):
        return f'{self.name} -- {self.slug} -- {self.is_active} -- {self.parent}'

class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False, blank=False,
        related_name='carts',
        verbose_name='Покупець'
    )
    is_active = models.BooleanField(default=True, verbose_name='Статус корзини')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення корзини')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення корзини')

    def get_total_price_cart(self):
        total_price_cart = 0
        cart_items = CartItem.objects.filter(cart=self)
        for cart_item in cart_items:
            total_price_cart += cart_item.get_total_price_product()
        return total_price_cart

    def __str__(self):
        return f'{self.user} -- {self.is_active}'

class CartItem(models.Model):
    cart = models.ForeignKey(
        'online_store_app.Cart',
        on_delete=models.CASCADE,
        null=False, blank=False,
        related_name='items',
        verbose_name='Корзина'
    )
    product_seller = models.ForeignKey(
        'online_store_app.ProductSeller',
        on_delete=models.CASCADE,
        null=False, blank=False,
        related_name='carts',
        verbose_name='Пропозиція продавця продукту'
    )
    quantity = models.PositiveIntegerField(
        validators=[MaxValueValidator(10000)],
        null=False, blank=False,
        verbose_name='Кількість продуктів в корзині'
    )
    price_at_time = models.PositiveIntegerField(default=0, verbose_name='Фіксована ціна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення корзини с продуктами')

    def get_total_price_product(self):
        return self.price_at_time * self.quantity

    def __str__(self):
        return  f'{self.cart} -- {self.product_seller} -- {self.quantity} -- {self.price_at_time}'

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='orders',
        verbose_name='Покупець'
    )
    status = models.CharField(default='немає дій', verbose_name='Статус замовлення')
    total_price = models.PositiveIntegerField(
        validators=[MaxValueValidator(1000000)], null=True, blank=False,
        verbose_name='Сумма замовлення'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення замовлення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення замовлення')

    def __str__(self):
        return f'{self.user} -- {self.status} -- {self.total_price}'

class OrderItem(models.Model):
    order = models.ForeignKey(
        'online_store_app.Order',
        on_delete=models.SET_NULL,
        null=True, blank=False,
        related_name='items',
        verbose_name='Вміст замовлення'
    )
    product_seller = models.ForeignKey(
        'online_store_app.ProductSeller',
        on_delete=models.CASCADE,
        null=False, blank=False,
        related_name='product_sellers',
        verbose_name='Пропозиція продавця продукту'
    )
    quantity = models.PositiveIntegerField(
        validators=[MaxValueValidator(10000)],
        null=False, blank=False,
        verbose_name='Кількість продуктів які були оплаченні'
    )
    price_at_time = models.PositiveIntegerField(null=True, blank=True, verbose_name='Фіксована ціна в замовленні')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення оплаченного замовлення')

    def __str__(self):
        return f'{self.order} -- {self.product_seller} -- {self.quantity} -- {self.price_at_time}'

class ProductReview(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False, blank=False,
        related_name='product_review_users',
        verbose_name='Покупець'
    )
    product = models.ForeignKey(
        'online_store_app.Product',
        on_delete=models.CASCADE,
        null=False, blank=False,
        related_name='product_reviews',
        verbose_name='Продукт'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=False, blank=False,
        verbose_name='Рейтинг продукту'
    )
    comment = models.TextField(max_length=500, blank=True, verbose_name='Відгук')
    is_active = models.BooleanField(default=True, verbose_name='Актуальний відгук чи ні?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення відгуку')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення відгуку')

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.user} -- {self.product} -- {self.rating} -- {self.is_active}'

class SellerReview(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False, blank=False,
        related_name='seller_review_users',
        verbose_name='Покупець'
    )
    seller = models.ForeignKey(
        'accountss.OnlineStoreUser',
        on_delete=models.CASCADE,
        null=False, blank=False,
        related_name='seller_reviews',
        verbose_name='Продавець'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=False, blank=False,
        verbose_name='Рейтинг продавця'
    )
    comment = models.TextField(max_length=500, blank=True, verbose_name='Відгук')
    is_active = models.BooleanField(default=True, verbose_name='Актуальний відгук чи ні?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення відгуку')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення відгуку')

    class Meta:
        unique_together = ('seller', 'user')

    def __str__(self):
        return f'{self.user} -- {self.seller} -- {self.rating} -- {self.is_active}'

