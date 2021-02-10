from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    mobile_no = models.IntegerField(max_length=10, null=True)
    city = models.CharField(max_length=100, null=True)
    pin_code = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=50, null=True)
    user_image = models.ImageField(null=True, blank=True)
    wallet = models.IntegerField(null=True)

    @property
    def ImageURL(self):
        try:
            url = self.user_image.url
        except ValueError:
            url = ''
        return url


class Category(models.Model):
    category_name = models.CharField(max_length=50, null=True)
    category_image = models.ImageField(null=True, blank=True)

    @property
    def ImageURL(self):
        try:
            url = self.category_image.url
        except ValueError:
            url = ''
        return url


class ProductDetail(models.Model):
    product_name = models.CharField(max_length=100, null=True)
    product_description = models.TextField(null=True)
    product_price = models.IntegerField(null=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    product_image = models.ImageField(null=True, blank=True)

    @property
    def ImageURL(self):
        try:
            url = self.product_image.url
        except ValueError:
            url = ''
        return url
