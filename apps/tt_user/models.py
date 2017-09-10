from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.EmailField(max_length=50)
    isValid = models.BooleanField(default=True)
    isActive = models.BooleanField(default=False)

class UserAddressInfo(models.Model):
    uname = models.CharField(max_length=20)
    uaddress = models.CharField(max_length=200)
    uphone = models.CharField(max_length=11)
    user = models.ForeignKey('UserInfo')

