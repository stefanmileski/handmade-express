# Generated by Django 4.2.1 on 2023-05-29 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0019_alter_cart_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='', max_length=200, unique=True),
        ),
    ]
