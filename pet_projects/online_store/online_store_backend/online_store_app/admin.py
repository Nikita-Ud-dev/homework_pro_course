from django.contrib import admin
from online_store_app.models import (
    Product,ProductSeller, Category,
    Order,
    ProductReview, SellerReview
)
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductSeller)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(ProductReview)
admin.site.register(SellerReview)