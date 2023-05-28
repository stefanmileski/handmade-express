from django.urls import path
from ShopApp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('products/<slug:slug>', views.product_detail, name='product_detail'),
    path('categories/', views.categories, name='categories'),
    path('categories/<slug:slug>', views.category_list, name='category_list'),
    path('user_profile/', views.user_profile, name='user_profile'),
]
