from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    mobile_no = models.BigIntegerField(null=True)
    user_image = models.ImageField(default="profileDefault.jpg", null=True, blank=True)
    wallet = models.IntegerField(null=True, default="0")

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


class ProductImages(models.Model):
    product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE, null=True)
    extra_images = models.ImageField(null=True, blank=True)

    @property
    def ImageURL(self):
        try:
            url = self.extra_images.url
        except ValueError:
            url = ''
        return url



class RefferalOffer(models.Model):
    reff_name = models.CharField(null=True, max_length=225)
    reff_discount = models.IntegerField(null=True)
    reff_price = models.IntegerField(null=True)
    reffered_person_discount = models.IntegerField(null=True)
    order_maximum = models.IntegerField(null=True)
    reff_offer_type = models.CharField(null=True, max_length=225)
    reff_status = models.BooleanField(null=True, default=True)


