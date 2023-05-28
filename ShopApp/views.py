from django.shortcuts import render

from ShopApp.models import Category, Product
import logging


# Create your views here.

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'ShopApp/index.html', context)
