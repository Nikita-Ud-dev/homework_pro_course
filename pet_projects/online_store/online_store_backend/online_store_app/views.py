
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from online_store_app.utils import get_cart, get_cart_items, validator_price_product, validator_is_active_product
from online_store_app.forms import (
    ProductForm,
    ProductSellerForm,
    ProductReviewForm,
    SellerReviewForm,
)
from online_store_app.models import (
    Product,
    ProductSeller,
    ProductReview,
    SellerReview,
    Cart, CartItem,
    Order, OrderItem,
)

# Create your views here.

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

class ProductCreateView(LoginRequiredMixin,  CreateView):
    model = Product
    form_class = ProductForm
    context_object_name = 'product'
    template_name = 'product/create_product.html'
    success_url = reverse_lazy('online_store_app:product_list')

class ProductUpdateView(LoginRequiredMixin,  UpdateView):
    model = Product
    form_class = ProductForm
    context_object_name = 'product_seller'
    template_name = 'product/update_product.html'
    success_url = reverse_lazy('online_store_app:product_list')
    pk_url_kwarg = 'product_id'

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    context_object_name = 'product_seller'
    template_name = 'product/confirm_delete_product.html'
    success_url = reverse_lazy('online_store_app:product_list')
    pk_url_kwarg = 'product_id'

class ProductSellerListView(LoginRequiredMixin, ListView):
    model = ProductSeller
    template_name = 'product_seller/product_seller_list.html'
    context_object_name = 'products_sellers'

class ProductSellerCreateView(LoginRequiredMixin, CreateView):
    model = ProductSeller
    form_class = ProductSellerForm
    template_name = 'product_seller/create_product_seller.html'
    success_url = reverse_lazy('online_store_app:product_list')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class ProductSellerUpdateView(LoginRequiredMixin,  UpdateView):
    model = ProductSeller
    form_class = ProductSellerForm
    template_name = 'product_seller/update_product_seller.html'
    success_url = reverse_lazy('online_store_app:product_list')
    pk_url_kwarg = 'product_seller_id'

class ProductSellerDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductSeller
    template_name = 'product_seller/confirm_delete_product_seller.html'
    success_url = reverse_lazy('online_store_app:product_list')
    context_object_name = 'product_seller'
    pk_url_kwarg = 'product_seller_id'

class ProductSellerInProductListView(LoginRequiredMixin, ListView):
    model = ProductSeller
    template_name = 'product_seller/product_seller_in_product_list.html'
    context_object_name = 'product_sellers'

    def get_queryset(self):
        return ProductSeller.objects.filter(product_id=self.kwargs['product_id'])

class CartView(LoginRequiredMixin,  TemplateView):
    model = Cart
    template_name = 'cart/cart_detail.html'

    def get(self, *args, **kwargs):
        if not Cart.objects.filter(user=self.request.user, is_active=True):
            Cart.objects.create(
                user = self.request.user,
                is_active = True,
            )
            return super().get(*args, **kwargs)
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        cart = Cart.objects.get(user=self.request.user, is_active=True)
        cart_items = CartItem.objects.filter(cart=cart)

        context['cart'] = cart
        context['items'] = cart_items
        return context

@login_required
def add_to_cart(request, product_seller_id):
    product_seller = get_object_or_404(ProductSeller, id=product_seller_id)
    if request.method == 'POST':
        cart, created_cart = Cart.objects.get_or_create(user=request.user, is_active=True)
        try:
            item = CartItem.objects.get(cart=cart, product_seller_id=product_seller_id)
            item.quantity += 1
            item.save()
        except CartItem.DoesNotExist:
            create_item = CartItem.objects.create(
                cart=cart,
                product_seller_id=product_seller_id,
                price_at_time = product_seller.price,
                quantity=1,
            )
            create_item.save()

    return redirect('online_store_app:product_list')

@login_required
def increase_cart_item(request, cart_item_id):
    cart_items = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        cart_items.quantity += 1
        cart_items.save()
        return redirect('online_store_app:cart')
    return redirect('online_store_app:cart')

@login_required
def decrease_cart_item(request, cart_item_id):
    cart_items = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        quantity = cart_items.quantity
        if quantity == 1:
            cart_items.delete()
            return redirect('online_store_app:cart')

        cart_items.quantity -= 1
        cart_items.save()
        return redirect('online_store_app:cart')
    return redirect('online_store_app:cart')

@login_required
def set_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    product_seller_quantity = cart_item.product_seller.quantity
    if request.method == 'POST':
        try:
            int(request.POST.get('quantity'))
        except ValueError:
            cart_item.quantity = 1
            cart_item.save()
            return redirect('online_store_app:cart')

        quantity = int(request.POST.get('quantity'))
        if quantity == 0 or quantity < 0 :
            cart_item.delete()
            return redirect('online_store_app:cart')

        elif quantity > product_seller_quantity:
            cart_item.quantity = product_seller_quantity
            cart_item.save()
            return redirect('online_store_app:cart')

        cart_item.quantity = quantity
        cart_item.save()
        return redirect('online_store_app:cart')
    return redirect('online_store_app:cart')

class OrderListView(LoginRequiredMixin,  ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'

class OrderDetailView(LoginRequiredMixin,  DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

class OrderCreateAndCreateOrderItemView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'

    def post(self, request, *args, **kwargs):
        cart = get_cart(request)
        cart_items = get_cart_items(request)

        changes_price = validator_price_product(cart_items)
        if changes_price:
            messages.info(request, 'Ціна на деякі товари були зміненні продавцем. Ми оновили її в кошику.')
            return redirect('online_store_app:cart')

        cart_items = get_cart_items(request)

        changes_is_active = validator_is_active_product(cart_items)
        if changes_is_active:
            messages.info(request, 'Деякі товари недоступні в наявності. Ми видалили ці товари із кошику.')
            return redirect('online_store_app:cart')

        cart_items = get_cart_items(request)
        total_price = cart.get_total_price_cart()

        order_created = Order.objects.create(
            user=request.user,
            status='Створено',
            total_price=total_price,
        )
        order_created.save()
        order = order_created

        for item in cart_items:
            product_seller = item.product_seller
            quantity = item.quantity
            price_at_time = item.get_total_price_product()
            OrderItem.objects.create(
            order=order,
            product_seller=product_seller,
            quantity=quantity,
            price_at_time=price_at_time,
        )

        cart_items.delete()
        cart.is_active = False
        cart.save()
        return redirect('online_store_app:order_detail', order_id=order.id)

class ProductReviewCreateView(LoginRequiredMixin,  CreateView):
    model = ProductReview
    form_class = ProductReviewForm
    template_name = 'product_review/create_product_review.html'
    success_url = reverse_lazy('online_store_app:product_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product_id = self.kwargs['product_id']
        return super().form_valid(form)

class ProductReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductReview
    form_class = ProductReviewForm
    template_name = 'product_review/update_product_review.html'
    success_url = reverse_lazy('online_store_app:product_list')
    pk_url_kwarg = 'product_review_id'

class ProductReviewDeleteView(LoginRequiredMixin,  DeleteView):
    model = ProductReview
    template_name = 'product_review/confirm_delete_product_review.html'
    success_url = reverse_lazy('online_store_app:product_list')
    pk_url_kwarg = 'product_review_id'
    context_object_name = 'product_review'

class SellerReviewCreateView(LoginRequiredMixin, CreateView):
    model = SellerReview
    form_class = SellerReviewForm
    template_name = 'seller_review/create_seller_review.html'
    success_url = reverse_lazy('online_store_app:product_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.seller_id = self.kwargs['seller_id']
        return super().form_valid(form)


class SellerReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = SellerReview
    form_class = SellerReviewForm
    template_name = 'seller_review/update_seller_review.html'
    success_url = reverse_lazy('online_store_app:product_list')
    pk_url_kwarg = 'seller_review_id'


class SellerReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = SellerReview
    template_name = 'seller_review/confirm_delete_seller_review.html'
    success_url = reverse_lazy('online_store_app:product_list')
    pk_url_kwarg = 'seller_review_id'
    context_object_name = 'seller_review'

