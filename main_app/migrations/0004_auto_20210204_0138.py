# Generated by Django 3.1.3 on 2021-02-03 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_category_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='product_image',
            new_name='category_image',
        ),
    ]