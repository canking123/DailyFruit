from django.db import models


# Create your models here.

class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle


class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='tt_goods')
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    isDelete = models.BooleanField(default=False)
    # 单位
    gunit = models.CharField(max_length=20, default='500g')
    # 点击量、人气
    gclick = models.IntegerField()
    # 简介
    gdesc = models.CharField(max_length=200)
    # 库存量
    gstorage = models.IntegerField()
    # 描述
    gcontent = models.TextField()
    # 类型
    gtype = models.ForeignKey(TypeInfo)

    def __str__(self):
        return self.gtitle
