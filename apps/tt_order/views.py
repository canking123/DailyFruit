from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from tt_cart.models import *
from django.db import transaction
from .models import *
from datetime import datetime
from tt_user.models import *
from tt_user.user_decorators import user_login


# Create your views here.
@user_login
def place_order(request):
    u_id = request.session['uid']
    u_addr = UserAddressInfo.objects.filter(user_id=u_id)
    # addr = u_addr.uaddress
    # tel = u_addr.uphone
    # name = u_addr.uname
    dict = request.GET
    cid = dict.getlist('cid')  # [1,3]
    cart_list = CartInfo.objects.filter(goods__in=cid)
    context = {'clist': cart_list, 'list': u_addr}
    return render(request, 'tt_order/place_order.html', context)


@transaction.atomic
@user_login
def do_order(request):
    u_id = request.session['uid']
    cid = request.POST.getlist('cid')
    print(cid)
    addr = request.POST.get('addr')
    sid = transaction.savepoint()
    cart_list = CartInfo.objects.filter(goods__in=cid)
    # print(cart_list)
    order = OrderInfo()
    order.user_id = u_id
    order.oid = '%s%s' % (datetime.now().strftime('%Y%m%d%H%M%S'), u_id)
    total = 0
    order.ototal = 0
    order.oaddress = addr
    order.save()
    isOK = True
    for cart in cart_list:
        print(cart)
        if cart.count < cart.goods.gstorage:
            detail = OrderDetailInfo()
            detail.goods = cart.goods
            detail.order = order
            detail.price = cart.goods.gprice
            detail.count = cart.count
            detail.save()
            total += detail.count * detail.price
            cart.goods.gstorage -= cart.count
            cart.goods.save()
            cart.delete()
        else:
            isOK = False
            break
    if isOK:
        order.ototal = total
        order.save()
        transaction.savepoint_commit(sid)

        return redirect('/user/user_center_order/')
    else:
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')

# def pay(request):
#     id = request.POST.get('id')
#     order = OrderInfo.objects.get(pk=id)
#     order.oIsPay=True
#     order.save()
#     return redirect('/user/order/')
