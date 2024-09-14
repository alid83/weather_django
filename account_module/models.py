from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    avatar = models.CharField(max_length=20, verbose_name='تصویر آواتار', null=True, blank=True)
    email_active_code = models.CharField(max_length=100, verbose_name='کد فعالسازی ایمیل')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.get_full_name()


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_joined = models.CharField(max_length=100)
    cities = models.CharField(max_length=100)
    date_search = models.CharField(max_length=100, null=True, blank=True)
    persian_date_search = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
