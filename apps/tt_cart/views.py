from django.shortcuts import render
from .models import CartInfo
from tt_goods.models import GoodsInfo
from django.http import JsonResponse
from django.db.models import Sum
from tt_user.user_decorators import user_login


# Create your views here.


@user_login
def cart(request):
    cart_list = CartInfo.objects.filter(user_id=int(request.session['uid']))
    context = {'title': '购物车', 'cart_list': cart_list, 'sub_page_name': '购物车'}
    return render(request, 'tt_cart/cart.html', context)

@user_login
def add(request):
    dict = request.GET
    gid = int(dict.get('gid', ''))
    count = int(dict.get('count'))
    kucun = GoodsInfo.objects.get(pk=gid).gstorage

    uid = int(request.session.get('uid'))
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) == 0:  # 如果没有就创建
        cart = CartInfo()
        cart.user_id = request.session.get('uid')
        cart.goods_id = int(gid)
        cart.count = count
        cart.save()
    else:  # 如果有就在原来的基础上加上数量，不需创建。
        cart = carts[0]
        count1 = cart.count + count
        if count1 > kucun:
            cart.count = kucun
        else:
            cart.count += count
        cart.save()

    return JsonResponse({'isok': 1})


def count(request):
    c = calc_count(request.session.get('uid'))
    return JsonResponse({'count': c})


def calc_count(uid):
    c = CartInfo.objects.filter(user_id=uid).aggregate(Sum('count'))# 字典
    if c.get('count__sum') == None: # 根据键拿值
        return 0
    else:
        return c.get('count__sum')


def add_count(request):
    dict = request.GET
    add_id = dict.get('add_id')
    cart = CartInfo.objects.get(pk=add_id)
    cart.count += 1
    cart.save()
    return JsonResponse({'isok': 1})


def minus_count(request):
    dict = request.GET
    minus_id = dict.get('minus_id')
    cart = CartInfo.objects.get(pk=minus_id)
    if cart.count <= 1:
        cart.count = 1
    else:
        cart.count -= 1
    cart.save()
    return JsonResponse({'isok': 1})


def change_count(request):
    dict = request.GET
    change_id = dict.get('change_id')
    count = int(dict.get('count'))
    cart = CartInfo.objects.get(pk=change_id)
    cart.count = count
    cart.save()
    return JsonResponse({'isok': 1})


def del_cart(request):
    try:
        cid = request.GET.get('cid')
        cart = CartInfo.objects.get(pk=cid)
        cart.delete()
        return JsonResponse({'isdelete': 1})
    except:
        return JsonResponse({'isdelete': 0})
