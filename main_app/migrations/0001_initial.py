# Generated by Django 4.1 on 2022-09-03 06:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, null=True)),
                ('category_image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, null=True)),
                ('product_description', models.TextField(null=True)),
                ('product_price', models.IntegerField(null=True)),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('offer_price', models.FloatField(blank=True, null=True)),
                ('offer_percentage', models.IntegerField(blank=True, null=True)),
                ('product_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='RefferalOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reff_name', models.CharField(max_length=225, null=True)),
                ('reff_discount', models.IntegerField(null=True)),
                ('reff_price', models.IntegerField(null=True)),
                ('reffered_person_discount', models.IntegerField(null=True)),
                ('order_maximum', models.IntegerField(null=True)),
                ('reff_offer_type', models.CharField(max_length=225, null=True)),
                ('reff_status', models.BooleanField(default=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_no', models.BigIntegerField(null=True)),
                ('user_image', models.ImageField(blank=True, default='profileDefault.jpg', null=True, upload_to='')),
                ('wallet', models.IntegerField(default='0', null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_images', models.ImageField(blank=True, null=True, upload_to='')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.productdetail')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(blank=True, max_length=20, null=True)),
                ('offer_start', models.DateField(null=True)),
                ('offer_expiry', models.DateField(null=True)),
                ('discount_amount', models.FloatField(null=True)),
                ('offer_type', models.CharField(blank=True, max_length=40, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.category')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.productdetail')),
            ],
        ),
    ]
