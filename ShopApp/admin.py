from django.contrib import admin

# Register your models here.
from ShopApp.models import CustomUser, Category, Material, \
    Color, Product, Order, ProductInOrder, Cart, ProductInCart, Review


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'material', 'color', 'seller']
    search_fields = ['name', 'category__name', 'material__name', 'color__name', 'seller__username']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', 'material', 'color', 'seller']

    def has_change_permission(self, request, obj=None):
        if obj and (request.user == obj.seller):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and (request.user == obj.seller):
            return True
        return False


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'rating', 'comment']
    list_filter = ['product', 'customer']
    search_fields = ['product__name', 'user__username']

    def has_change_permission(self, request, obj=None):
        if obj and (request.user == obj.customer.user):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and (request.user == obj.customer.user):
            return True
        return False


admin.site.register(CustomUser)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Material)
admin.site.register(Color)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(ProductInOrder)
admin.site.register(Cart)
admin.site.register(ProductInCart)
admin.site.register(Review, ReviewAdmin)
