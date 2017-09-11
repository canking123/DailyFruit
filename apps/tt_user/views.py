
from hashlib import sha1
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import UserInfo

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse


# Create your views here.

def register(request):

    return render(request, 'tt_user/register.html')

def username_repeat(request):
    # 获取用户输入的名字
    uname = request.GET.get('uname')
    # 查看数据表中是否有同样姓名的数据
    count = UserInfo.objects.filter(uname=uname).count()
    # 使用ajax就要返回JsonResponse类型的对象
    return JsonResponse({'count':count})

def add_user(request):

    user_info = UserInfo()
    user_info.uname = request.POST.get('user_name')

    s1 = sha1()
    s1.update(request.POST.get('pwd').encode('utf8'))
    user_info.upwd = s1.hexdigest()
    user_info.uemail = request.POST.get('email')
    user_info.isActive = 1
    user_info.save()
    return redirect('/user/login')

def login(request):
    # user_info = UserInfo()
    # user_info.uname = request.POST.get('username')
    #
    # s1 = sha1()
    # s1.update(request.POST.get('pwd').encode('utf8'))
    # user_info.upwd = s1.hexdigest()
    print('5555555')




    return render(request, 'tt_user/login.html')

def user_center_info(request):
    return render(request, 'tt_user/user_center_info.html')

def user_center_order(request):
    return render(request, 'tt_user/user_center_order.html')

def user_center_site(request):
    return render(request, 'tt_user/user_center_site.html')

def send(request):
    msg='<a href="http://127.0.0.1:8000/user/active/" target="_blank">点击激活</a>'
    send_mail('nihao',
              '',
              settings.EMAIL_FROM,
              ['302713200@qq.com'],
              html_message=msg)

    # 后期部署改用真实的ip地址   user_info = UserInfo.objects.filter()

    return HttpResponse('ok')

def active(request):
    return HttpResponse('激活')