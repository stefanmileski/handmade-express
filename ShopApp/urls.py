from django.urls import path
from ShopApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('<str:seller_username>/<slug:slug>', views.product_detail, name='product_detail'),
    path('categories/', views.categories, name='categories'),
    path('categories/<slug:slug>', views.category_list, name='category_list'),
    path('<str:seller_username>', views.seller_profile, name='seller_profile'),
    path('reviews/<slug:slug>', views.reviews, name='reviews'),
    path('cart/', views.cart, name='cart'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('orders/', views.orders, name='orders'),
    path('add_product/', views.add_product_to_shop, name='add_product_to_shop'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
]
