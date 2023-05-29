from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your models here.


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:  # New, 1
        verbose_name_plural = 'Categories'

    def __str__(self):
        return str(self.name)


class Material(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Color(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    sold = models.IntegerField(default=0)
    slug = models.SlugField(default="", max_length=200, unique=True)

    def calculate_average_rating(self):
        if len(self.reviews.all()) == 0:
            return 'No reviews yet'
        total = 0
        for review in self.reviews.all():
            total += review.rating
        return total / len(self.reviews.all()) if len(self.reviews.all()) > 0 else 0

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100,
                              choices=[('Pending', 'Pending'),
                                       ('Processing', 'Processing'),
                                       ('Delivered', 'Delivered'),
                                       ('Cancelled', 'Cancelled')])
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='ProductInOrder', related_name='orders')

    def calculate_total(self):
        total = 0
        for product_in_order in self.productinorder_set.all():
            total += product_in_order.subtotal()
        return total

    def __str__(self):
        return f"Order #{self.id}: {self.status}"


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    class Meta:  # New, 1
        verbose_name_plural = 'ProductInOrder'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product, through='ProductInCart')

    def calculate_total(self):
        # Perform the necessary calculations to get the total price
        total = 0
        for product_in_cart in self.productincart_set.all():
            total += product_in_cart.subtotal()
        return total

    def __str__(self):
        return f"{self.customer.user.username}'s cart"


class ProductInCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    class Meta:  # New, 1
        verbose_name_plural = 'ProductInCart'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Review(models.Model):
    # Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"Review #{self.id}: {self.rating} stars"

    class Meta:
        unique_together = ['customer', 'product']


@receiver(post_save, sender=CustomUser)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(customer=instance)
