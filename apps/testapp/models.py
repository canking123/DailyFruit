from django.db import models

# Create your models here.
class HeroInfo(models.Model):
    hname=models.CharField(max_length=20)
    hcontent=models.CharField(max_length=100)