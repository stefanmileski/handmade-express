import random

from django.shortcuts import render

from ShopApp.models import Category, Product


def index(request):
    items = list(Product.objects.order_by('-sold')[:5])
    random.shuffle(items)

    return render(request, 'ShopApp/index.html', {
        "products": items
    })


def products(request, search_term=None):
    if search_term:
        items = Product.objects.filter(name__icontains=search_term)
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


def user_profile(request, slug):
    return render(request, 'ShopApp/user_profile.html', {
        "user": request.user
    })
