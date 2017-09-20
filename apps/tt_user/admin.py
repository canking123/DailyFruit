from django.contrib import admin
from .models import UserInfo,UserAddressInfo
# Register your models here.

class UserInfoAdmin(admin.ModelAdmin):
    list_display=['pk','uname','upwd','uemail','isActive','isValid']

class UserAddressAdmin(admin.ModelAdmin):
    list_display=['pk','uname','uaddress','uphone','user']

admin.site.register(UserInfo,UserInfoAdmin)
admin.site.register(UserAddressInfo,UserAddressAdmin)
