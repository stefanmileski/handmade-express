import random

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from ShopApp.models import Category, Product, CustomUser, Cart

from django.db.models import Q


def index(request):
    items = list(Product.objects.order_by('-sold')[:5])
    random.shuffle(items)

    return render(request, 'ShopApp/index.html', {
        "products": items
    })


def products(request):
    search_term = request.GET.get('search_term')
    if search_term:
        items = Product.objects.filter(Q(name__icontains=search_term) | Q(description__icontains=search_term))
    else:
        items = Product.objects.all()
    return render(request, 'ShopApp/products.html', {
        "products": items
    })


def product_detail(request, slug):
    return render(request, 'ShopApp/product_detail.html', {
        "product": Product.objects.get(slug=slug)
    })


def categories(request):
    return render(request, 'ShopApp/categories.html', {
        "categories": Category.objects.all()
    })


def category_list(request, slug):
    category = Category.objects.get(slug=slug)
    items = list(Product.objects.filter(category=category))

    return render(request, 'ShopApp/category_list.html', {
        "products": items,
        "category": category
    })


def reviews(request, slug):
    product = Product.objects.get(slug=slug)
    reviews_list = list(product.reviews.all())
    reviews_list.sort(key=lambda x: x.created_at)
    return render(request, 'ShopApp/product_reviews.html', {
        "product": product,
        "reviews": product.reviews.all()
    })


def seller_profile(request, seller_username):
    seller = CustomUser.objects.get(user__username=seller_username)
    seller_products = list(seller.products.all())
    s_after_apostrophe = not seller.full_name.endswith('s')
    return render(request, 'ShopApp/seller_profile.html', {
        "seller": seller,
        "products": seller_products,
        "s_after_apostrophe": s_after_apostrophe,
    })


# def login(request):
#     return render(request, 'ShopApp/login.html')
#

def cart(request):
    user_cart = CustomUser.objects.get(user=request.user).cart
    return render(request, 'ShopApp/cart.html', {
        "cart": user_cart
    })


class CustomLoginView(LoginView):
    def get_success_url(self):
        # Specify the URL where you want to redirect after login
        return '/'

    def form_valid(self, form):
        # Add any additional logic you need before login
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    # Specify the URL where you want to redirect after logout
    return redirect('/')


def orders(request):
    return render(request, 'ShopApp/orders.html', {
        "orders": CustomUser.objects.get(user=request.user).orders.all()
    })