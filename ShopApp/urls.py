from django.urls import path
from ShopApp.views import index

urlpatterns = [
    path('', index, name='index'),
]
