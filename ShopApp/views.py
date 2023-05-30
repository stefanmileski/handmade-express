import random

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from ShopApp.models import Category, Product, CustomUser, Cart, Material, Color, Order, ProductInOrder, ProductInCart

from django.db.models import Q


def index(request):
    items = list(Product.objects.order_by('-sold')[:5])
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
    s_after_apostrophe = not seller.display_name.endswith('s')
    return render(request, 'ShopApp/seller_profile.html', {
        "seller": seller,
        "products": seller_products,
        "s_after_apostrophe": s_after_apostrophe,
    })


def cart(request):
    user_cart = Cart.objects.get(customer__user__username=request.user.username)
    items = user_cart.product_in_cart.all()
    return render(request, 'ShopApp/cart.html', {
        "items": items,
        "total": user_cart.calculate_total(),
    })


class CustomLoginView(LoginView):
    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('/')


def orders(request):
    customer = request.user.profile
    s_after_apostrophe = not customer.display_name.endswith('s')
    return render(request, 'ShopApp/orders.html', {
        "orders": request.user.profile.orders.all(),
        "s_after_apostrophe": s_after_apostrophe,
    })


def add_product_to_shop(request):
    if request.method == 'POST':
        product = Product()
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.category = Category.objects.get(name=request.POST.get('category'))
        product.material = Material.objects.get(name=request.POST.get('material'))
        product.color = Color.objects.get(name=request.POST.get('color'))
        product.image = request.FILES.get('image')
        product.quantity = request.POST.get('quantity')
        product.seller = request.user.profile
        product.save()
        return redirect('/')
    else:
        return render(request, 'ShopApp/add_product_form.html', {
            "categories": Category.objects.all(),
            "materials": Material.objects.all(),
            "colors": Color.objects.all(),
        })


def checkout(request):
    user_cart = Cart.objects.get(customer__user__username=request.user.username)
    items = user_cart.product_in_cart.all()
    Order(customer=request.user.profile).save()
    for item in items:
        ProductInOrder(product=item.product, order=request.user.profile.orders.last(), quantity=item.quantity).save()
        item.product.quantity -= item.quantity
        item.product.sold += item.quantity
        item.product.save()
        item.delete()
    return redirect('/')


def add_to_cart(request):
    user_cart = Cart.objects.get(customer__user__username=request.user.username)
    product = Product.objects.get(id=request.POST.get('product_id'))
    if request.POST.get('quantity'):
        quantity = int(request.POST.get('quantity'))
    else:
        quantity = 1
    if ProductInCart.objects.filter(product=product, cart=user_cart).exists():
        product_in_cart = ProductInCart.objects.get(product=product, cart=user_cart)
        product_in_cart.quantity += quantity
        product_in_cart.save()
    else:
        ProductInCart(product=product, cart=user_cart, quantity=quantity).save()
    return redirect(request.META['HTTP_REFERER'])
