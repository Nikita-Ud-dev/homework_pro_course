from django import forms
from online_store_app.models import (
    Product,
    ProductSeller,
    ProductReview,
    SellerReview,
)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'category', 'images',
        ]
        widgets = {}
        help_texts = {
            'title': '',
            'description': '',
            'sellers': '',
            'category': '',
            'quantity': '',
            'images': '',
            'rating': '',
            'rating_count': '',
        }

        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)


class ProductSellerForm(forms.ModelForm):
    class Meta:
        model = ProductSeller
        fields = [
            'product',  'quantity',
            'is_active', 'discount', 'price',
        ]
        widgets = {}
        help_texts = {
            'title': '',
            'description': '',
            'sellers': '',
            'category': '',
            'quantity': '',
            'images': '',
            'rating': '',
            'rating_count': '',
        }

        def __init__(self, *args, **kwargs):
            seller = kwargs.pop('seller', None)
            super().__init__(*args, **kwargs)

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = [
            'rating',
            'comment',
            'is_active',
        ]
        widgets = {}
        help_texts = {
            'title': '',
            'description': '',
            'sellers': '',
            'category': '',
            'quantity': '',
            'images': '',
            'rating': '',
            'rating_count': '',
        }

        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)

class SellerReviewForm(forms.ModelForm):
    class Meta:
        model = SellerReview
        fields = [
            'rating',
            'comment',
            'is_active',
        ]
        widgets = {}
        help_texts = {
            'title': '',
            'description': '',
            'sellers': '',
            'category': '',
            'quantity': '',
            'images': '',
            'rating': '',
            'rating_count': '',
        }

        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)