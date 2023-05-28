# Generated by Django 4.2.1 on 2023-05-28 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0008_product_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=0, max_length=200, unique=True),
            preserve_default=False,
        ),
    ]