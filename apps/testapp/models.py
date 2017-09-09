from django.db import models

# Create your models here.


class Development(models.Model):
    nick_name = models.CharField(max_length=10)

    class Meta:
        db_table = 'development'

    def __str__(self):
        return self.btitle


class Developer(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField(default=10)

    class Meta:
        db_table = 'developer'

