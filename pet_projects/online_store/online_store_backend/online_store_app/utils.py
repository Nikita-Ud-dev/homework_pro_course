from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from online_store_app.models import (
    Cart, CartItem,
)

def get_cart(request):
    return Cart.objects.get(user=request.user, is_active=True)

def get_cart_items(request):
    cart = get_cart(request)
    return CartItem.objects.filter(cart=cart)

def validator_price_product(cart_items):
    changes = False

    for cart_item in cart_items:
        if cart_item.price_at_time != cart_item.product_seller.price:
            cart_item.price_at_time = cart_item.product_seller.price
            cart_item.save()
            changes = True

    return changes

def validator_is_active_product(cart_items):
    changes = False

    for cart_item in cart_items:
        if cart_item.product_seller.is_active == False:
            cart_item.delete()
            changes = True

    return changes

