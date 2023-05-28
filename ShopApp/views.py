import random

from django.shortcuts import render

from ShopApp.models import Category, Product


# Create your views here.

def index(request):
    items = list(Product.objects.order_by('-sold')[:5])
    random.shuffle(items)
    return render(request, 'ShopApp/index.html', {
        "products": items
    })


def products(request):
    return render(request, 'ShopApp/products.html', {
        "products": Product.objects.all()
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
    return render(request, 'ShopApp/category_list.html', {
        "category": Category.objects.get(slug=slug)
    })

def user_profile(request):
    return render(request, 'ShopApp/user_profile.html', {
        "user": request.user
    })