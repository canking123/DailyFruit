from django.contrib import admin
from .models import TypeInfo,GoodsInfo
# Register your models here.

class TypeInfoAdmin(admin.ModelAdmin):
    list_display=['pk','ttitle','isDelete']

class GoodsInfoAdmin(admin.ModelAdmin):
    list_display=['pk','gtitle','gstorage','gclick','gtype','isDelete']

admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)
