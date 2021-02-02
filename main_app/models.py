from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    city = models.CharField(max_length=100, null=True)
    pin_code = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=50, null=True)
    user_image = models.ImageField(null=True, blank=True)

    @property
    def ImageURL(self):
        try:
            url = self.user_image.url
        except ValueError:
            url = ''
        return url
