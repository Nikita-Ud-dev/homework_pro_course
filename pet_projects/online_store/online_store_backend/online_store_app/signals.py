from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from online_store_app.models import ProductReview, SellerReview, Product, ProductSeller

User = get_user_model()

@receiver(post_save, sender=ProductReview)
@receiver(post_delete, sender=ProductReview)
def recalculate_product_rating(sender, instance, **kwargs):
    product = instance.product
    sum_rating = 0
    product_review_queryset = ProductReview.objects.filter(product=product, is_active=True)
    review_count = product_review_queryset.count()

    for review in product_review_queryset:
        sum_rating += review.rating

    if review_count == 0:
        product.rating = None
        product.rating_count = 0
        product.save()
        return

    avg = sum_rating / review_count
    product.rating = avg
    product.rating_count = review_count
    product.save()

@receiver(post_save, sender=SellerReview)
@receiver(post_delete, sender=SellerReview)
def recalculate_seller_rating(sender, instance, **kwargs):
    seller = instance.seller
    sum_rating = 0
    seller_review_queryset =  SellerReview.objects.filter(seller=seller, is_active=True)
    review_count = seller_review_queryset.count()

    for review in seller_review_queryset:
        sum_rating += review.rating

    if review_count == 0:
        seller.rating = None
        seller.rating_count = 0
        seller.save()
        return

    avg = sum_rating / review_count
    seller.rating = avg
    seller.rating_count = review_count
    seller.save()

@receiver(post_save, sender=ProductSeller)
@receiver(post_delete, sender=ProductSeller)
def recalculate_product_quantity(sender, instance, **kwargs):
    product = instance.product
    sum_quantity = 0

    for obj in ProductSeller.objects.filter(product=product, is_active=True):
        sum_quantity += obj.quantity

    product.quantity = sum_quantity
    product.save()

# @receiver(post_delete, sender=ProductReview)
# def counts_saves_product_review_delete(sender, instance, **kwargs):
#     product = instance.product
#     sum_rating = 0
#
#     review_count = ProductReview.objects.filter(product=product, is_active=True).count()
#     for review in sender.objects.filter(product=product, is_active=True):
#         sum_rating += review.rating
#
#     if review_count == 0:
#         product.rating = None
#         product.rating_count = 0
#         product.save()
#         return
#
#     avg = sum_rating / review_count
#     product.rating = avg
#     product.rating_count = review_count
#     product.save()




