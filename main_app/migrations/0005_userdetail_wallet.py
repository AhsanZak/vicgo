# Generated by Django 3.1.3 on 2021-02-10 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20210204_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='wallet',
            field=models.IntegerField(null=True),
        ),
    ]
