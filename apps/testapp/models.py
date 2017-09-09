from django.db import models

# Create your models here.


class Development(models.Model):
    nick_name = models.CharField(max_length=10)

    class Meta:# 元信息类
        db_table = 'development'# 指定表的名称

    def __str__(self):
        return self.btitle
