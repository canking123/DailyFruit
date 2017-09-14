from django.db import models
from tt_goods.models import GoodsInfo
from tt_user.models import UserInfo
# Create your models here.


class CartInfo(models.Model):
    user = models.ForeignKey(UserInfo)
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()
