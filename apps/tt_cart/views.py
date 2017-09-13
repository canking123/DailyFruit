from django.shortcuts import render
from .models import CartInfo
from tt_goods.models import GoodsInfo
from django.http import JsonResponse
from django.db.models import Sum
# Create your views here.


def cart(request):
    return render(request, 'tt_cart/cart.html')


def add(request):
    dict = request.GET
    gid = int(dict.get('gid', ''))
    count = int(dict.get('count'))
    kucun = GoodsInfo.objects.get(pk=gid).gstorage

    uid = int(request.session.get('uid'))
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) == 0:
        cart = CartInfo()
        cart.user_id = request.session.get('uid')
        cart.goods_id = int(gid)
        cart.count = count
        cart.save()
    else:
        cart = carts[0]
        count1 = cart.count+count
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
    c = CartInfo.objects.filter(user_id=uid).aggregate(Sum('count'))

    if c.get('count__sum') == None:
        return 0
    else:
        return c.get('count__sum')