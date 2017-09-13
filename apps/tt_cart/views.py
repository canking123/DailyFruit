from django.shortcuts import render
from .models import CartInfo
from tt_goods.models import GoodsInfo
from django.http import JsonResponse
# Create your views here.


def cart(request):
    return render(request, 'tt_cart/cart.html')


def add(request):
    dict = request.GET
    gid = int(dict.get('gid', ''))
    count = int(dict.get('count'))
    print('gid' + gid)
    kucun = GoodsInfo.objects.get(pk=gid).gkucun
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
