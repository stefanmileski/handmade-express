# Generated by Django 4.2.1 on 2023-05-28 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0012_alter_customuser_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=123123123123, max_length=200),
            preserve_default=False,
        ),
    ]