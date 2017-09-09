from django.db import models

# Create your models here.


class Development(models.Model):
    nick_name = models.CharField(max_length=10)

    class Meta:
        db_table = 'development'


class Developer(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField(default=10)

    class Meta:
        db_table = 'developer'


class HeroInfo(models.Model):
    hname = models.CharField(max_length=20)
    hcontent = models.CharField(max_length=100)

