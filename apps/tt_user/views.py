from hashlib import sha1
from django.http import JsonResponse
from django.shortcuts import render, redirect
from apps.tt_user import user_decorators
from tt_goods.models import GoodsInfo
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from tt_order.models import OrderInfo
from django.core.paginator import Paginator

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
    if value is None:
        return render(request, 'tt_user/login.html')

    return render(request,'tt_user/login.html', {'uname': value})

def login_handle(request):
    if request.method == "GET":
        return redirect('/user/login/')

    username = request.POST.get('username')
    pwd = request.POST.get('pwd')
    uemail = request.POST.get('uemail')

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

            remember_user = request.POST.get('remember', 0)  # 0 是给它设置的默认值
            response = redirect(request.session.get('url_path','/user/user_center_info/'))
            print('1: ', response.items())
            if remember_user == '1':  # 注意  remember_user传过来的是一个字符串
                response.set_cookie('remember', username, expires=7 * 24 * 60 * 60)
            else:
                response.set_cookie('remember', '', expires=-1)

            request.session['uid'] = user.id
            request.session['uname'] = username
            return response

@user_decorators.user_login
def user_center_info(request):
     user_info= UserAddressInfo.objects.filter(user_id=int(request.session.get('uid'))).order_by('-pk')
     user_id = request.session.get('uid')
     user = UserInfo.objects.get(id=user_id)
     user_name = user.uname
     #取cookie,ｋey为goodsid,'_270_268'
     cookie_id_list = request.COOKIES.get('goodsid'+str(user_id))
     if cookie_id_list is None:
         goods_list = []

     else:
         #截取字符串，split('_')
         cookie_id_list1 = cookie_id_list.split('_')
         # ['',270,280].reverse()
         cookie_id_list1.reverse()
         cookie_id_list2 = cookie_id_list1[0:-1]
         goods_list = GoodsInfo.objects.filter(id__in=cookie_id_list2)
         #　传给模板　goods_list[0:5]
     context = {'user_name1': user_name, 'user_info' : user_info,'goodslist':goods_list[0:5], 'sub_page_name': '用户中心'}
     return render(request,'tt_user/user_center_info.html',context)

@user_decorators.user_login
def user_center_order(request, index):
    user_id = request.session.get('uid')
    user = UserInfo.objects.filter(id=int(user_id))
    user_name = user[0].uname

    orderlist = OrderInfo.objects.filter(user=user_id)
    p = Paginator(orderlist, 3)
    if index == '':
        index = '1'
    index = int(index)
    order_list = p.page(index)
    page_list = p.page_range
    context = {'user_name1': user_name, 'sub_page_name': '我的订单',
               'orderlist': order_list, 'index': index, 'pagelist': page_list}
    return render(request, 'tt_user/user_center_order.html', context)

@user_decorators.user_login
def user_center_site(request):
    user_id = request.session.get('uid')
    user = UserInfo.objects.get(id=user_id)
    user_name = user.uname
    uad_li = UserAddressInfo.objects.filter(user=user).order_by('-pk')
    print(type(uad_li))
    print(uad_li)
    if not uad_li.exists():
        context = {'user_name1': user_name, 'recv_person': '', 'sub_page_name': '用户中心',
                   'detailed_address': '', 'cell_phone': ''}
    else:
        context = {'user_name1': user_name,'recv_person':uad_li[0].uname, 'sub_page_name': '用户中心',
                   'detailed_address':uad_li[0].uaddress, 'cell_phone':uad_li[0].uphone}
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
    if 'uid' in request.session:
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
    context = {'recv_person':recvPerson, 'detailed_address':address, 'cell_phone':phone, 'sub_page_name': '用户中心'}
    return render(request,'tt_user/user_center_site.html',context)

