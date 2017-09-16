from django.shortcuts import render,redirect
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
    u_addr= UserAddressInfo.objects.get(user_id=u_id)
    dict =request.GET
    cid  =dict.getlist('cid')#[1,3]
    cart_list=CartInfo.objects.filter(id__in=cid)
    addr = u_addr.uaddress
    tel  = u_addr.uphone
    name = u_addr.uname
    context={'clist':cart_list,'addr':addr,'tel':tel,'name':name}
    return render(request,'tt_order/place_order.html',context)

@transaction.atomic
def do_order(request):
    cid=request.POST.getlist('cid')
    #开启事务
    sid=transaction.savepoint()
    #创建订单主表
    order=OrderInfo()
    order.oid='%s%s'%(datetime.now().strftime('%Y%m%d%H%M%S'),'1')
    order.user_id=1
    order.ototal=0
    order.oaddress=''
    order.save()
    #查询选中的购物车信息，逐个遍历
    cart_list=CartInfo.objects.filter(user__in=cid)
    total=0
    isOk=True
    for cart in cart_list:
        #判断商品库存是否满足当前购买数量
        if cart.count<=cart.goods.gkucun:
            #库存量足够，可以购买
            detail=OrderDetailInfo()
            detail.order=order
            detail.goods=cart.goods
            detail.price=cart.goods.gprice
            detail.count=cart.count
            detail.save()
            #计算总价
            total+=detail.count*detail.price
            #更改库存数量
            cart.goods.gkucun-=cart.count
            cart.goods.save()
            #删除购物车数据
            cart.delete()
        else:
            isOk=False
            break
    if isOk:
        #保存总价
        order.ototal=total
        order.save()
        #订单成功，转到用户中心
        transaction.savepoint_commit(sid)
        return redirect('/user/order/')
    else:
        #订单失败，是转到购物车，再次修改数量
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')