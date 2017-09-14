from hashlib import sha1
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse

# Create your views here.

def register(request):

    return render(request, 'tt_user/register.html')

def username_repeat(request):
    dict = request.GET
    # 获取用户输入的名字
    uname = dict.get('uname')
    # 查看数据表中是否有同样姓名的数据
    count = UserInfo.objects.filter(uname=uname).count()
    # 使用ajax就要返回JsonResponse类型的对象
    return JsonResponse({'count':count})

def add_user(request):
    dict = request.POST
    # 创建实例对象
    user_info = UserInfo()
    # 获取用户输入的姓名
    user_info.uname = dict.get('user_name')
    send_name = dict.get('user_name')
    # 获取用户输入的密码并进行加密
    s1 = sha1()
    s1.update(dict.get('pwd').encode('utf8'))
    user_info.upwd = s1.hexdigest()
    # 获取用户输入的邮箱
    user_info.uemail = dict.get('email')
    # 将获取到的用户信息保存到数据库中
    user_info.save()

    send(request,send_name)
    # 重定向到登录页面
    return redirect('/user/login')

def login(request):
    value = request.COOKIES.get('remember')
    # if value is None:
    #     return render(request, 'tt_user/login.html')
    return render(request,'tt_user/login.html', {'uname': value})

def login_handle(request):
    username = request.POST.get('username')
    pwd = request.POST.get('pwd')

    s1 = sha1()
    s1.update(pwd.encode())
    pwd_sha1 = s1.hexdigest()

    count = UserInfo.objects.filter(uname=username).count()
    if count == 0:
        # 定义error：1为用户名错误
        return JsonResponse({'error': 1})
    else:
        user = UserInfo.objects.get(uname=username)
        if user.upwd != pwd_sha1:
            # 定义error：2为密码错误
            return JsonResponse({'error': 2})
        else:
            dict = request.POST
            # 获取用户输入的姓名
            username = dict.get('username')
            # 获取用户输入的密码
            pwd = dict.get('pwd')
            uemail = dict.get('uemail')

            remember_user = dict.get('remember', 0)  # 0 是给它设置的默认值

            # print(remember_user)
            try:
                # uname是数据库中的字段，username是获取到的用户输入
                user = UserInfo.objects.get(uname=username)
                s1 = sha1()
                s1.update(pwd.encode('utf8'))
                pwd = s1.hexdigest()
                # upwd是数据库中的字段，pwd是用户输入的密码，要对其进行加密后比较二者是否一样如果一样说明密码正确
                if user.upwd != pwd or user.upwd is None:
                    print('密码错误！请核对您的密码！')
                    return render(request, 'tt_user/login.html', {'upwd_error': '密码为空，或者错误！'})

            except Exception as e:
                print(e)
                return HttpResponse('用户名输入有误，请重新输入')
                # return redirect('user/login_handle/')

            else:
                response = redirect('/user/user_center_info/')
                if remember_user == '1':  # 注意  remember_user传过来的是一个字符串
                    response.set_cookie('remember', username, expires=7 * 24 * 60 * 60)
                else:
                    response.set_cookie('remember', username, expires=-1)

                request.session['uid'] = user.id
                return response
            # 定义error：0为没有错误
            # return JsonResponse({'error': 0})
            return render(request,'tt_user/user_center_info.html')



def user_center_info(request):
     user_info= UserAddressInfo.objects.filter(user_id=int(request.session.get('uid'))).order_by('-pk')
     user_id = request.session.get('uid')
     user = UserInfo.objects.get(id=user_id)
     user_name = user.uname
     context = {'user_name1': user_name, 'user_info' : user_info}
     return render(request,'tt_user/user_center_info.html',context)

def user_center_order(request):
    user_id = request.session.get('uid')
    user = UserInfo.objects.get(id=int(user_id))
    user_name = user.uname
    context = {'user_name1': user_name}
    return render(request, 'tt_user/user_center_order.html',context)

def user_center_site(request):
    user_id = request.session.get('uid')
    user = UserInfo.objects.get(id=user_id)
    user_name = user.uname
    uad_li = UserAddressInfo.objects.filter(user=user).order_by('-pk')
    context = {'user_name1': user_name,'recv_person':uad_li[0].uname, 'detailed_address':uad_li[0].uaddress, 'cell_phone':uad_li[0].uphone}
    return render(request, 'tt_user/user_center_site.html', context)

def logout(request):
    del request.session['uid']
    return redirect('/user/login/')
    # return render(request,'tt_user/login.html')

def send(request,user_name):
    user = UserInfo.objects.get(uname=user_name)
    msg='<a href="http://127.0.0.1:8000/user/active/%s" target="_blank">点击激活</a>'%(user.id)
    send_mail('天天生鲜用户激活',
              '',
              settings.EMAIL_FROM,
              ['302713200@qq.com'],
              html_message=msg)

    # 后期部署改用真实的ip地址   user_info = UserInfo.objects.filter()
    return HttpResponse('用户注册成功，请到邮箱中激活')

def active(request,uid):
    user = UserInfo.objects.get(id=uid)
    user.isActive = True
    user.save()
    return HttpResponse('激活成功，<a href="/user/login/">点击登录</a>')


def islogin(request):
    result = 0
    if request.session.has_key('uid'):
        result = 1
    return JsonResponse({'islogin':result})



def update_address(request):
    dict = request.GET
    uid = request.session['uid']
    recvPerson = dict.get('recv_person')

    address = dict.get('detailed_address')
    postAddress = dict.get('post_address')
    phone = dict.get('cell_phone')

    userAddr = UserAddressInfo()
    userAddr.uaddress = address
    userAddr.uphone = phone
    userAddr.user_id = uid
    userAddr.uname = recvPerson

    userAddr.save()

    context = {'recv_person':recvPerson, 'detailed_address':address, 'cell_phone':phone}

    return render(request,'tt_user/user_center_site.html',context)

