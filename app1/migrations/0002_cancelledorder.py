# Generated by Django 3.1.3 on 2021-02-13 07:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0010_auto_20210213_1106'),
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CancelledOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateField(auto_now_add=True)),
                ('total_price', models.IntegerField(blank=True, null=True)),
                ('order_status', models.CharField(max_length=50, null=True)),
                ('transaction_id', models.CharField(max_length=200, null=True)),
                ('payment_mode', models.CharField(max_length=50, null=True)),
                ('payment_status', models.CharField(max_length=50, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.shippingaddress')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.productdetail')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
