# Generated by Django 4.2.1 on 2023-05-22 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0004_alter_review_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='uploaded',
        ),
        migrations.RemoveField(
            model_name='review',
            name='uploaded',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=0, upload_to='uploaded/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploaded/'),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
