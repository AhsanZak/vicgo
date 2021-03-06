# Generated by Django 3.1.3 on 2021-02-17 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_auto_20210213_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_images', models.ImageField(blank=True, null=True, upload_to='')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.productdetail')),
            ],
        ),
    ]
