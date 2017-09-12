from django.shortcuts import render
from .models import *
from tt_cart.models import *


# Create your views here.
def index(request):
    cont = {}
    cont2 = {}
    for i in range(1, 7):
        cats = CartInfo.objects.all()
        print(cats)
        print('1234')

        glist = GoodsInfo.objects.filter(gtype=i)
        glist = glist[0:4]
        cont2 = {'glist%s' % (i): glist}
        cont.update(cont2)
    context = cont
    return render(request, 'tt_goods/index.html', context)


def list(request, l_id):
    if (l_id == '0'):
        glist = GoodsInfo.objects.all()#全部商品
    else:
        glist = GoodsInfo.objects.filter(gtype_id=l_id)#筛选一类商品

    gtype = TypeInfo.objects.filter(id=l_id)#一类商品的类型
    count = GoodsInfo.objects.count()#总数

    n_glist = GoodsInfo.objects.all()
    n_glist = n_glist[count - 3:count]#取出最新的三件商品

    context = {'glist': glist, 'n_glist': n_glist,'gtype':gtype}
    return render(request, 'tt_goods/list.html', context)


def detail(request, g_id):
    goods = GoodsInfo.objects.filter(id=g_id)#取一件商品
    count = GoodsInfo.objects.count()#商品总数
    n_glist = GoodsInfo.objects.all()[count - 3:count]#取出最新三件商品

    # data = GoodsInfo.objects.get('gtype')
    # gtype=data.typeinfo_set.all()
    context = {'goods': goods, 'n_glist': n_glist,'gtype':gtype}
    return render(request, 'tt_goods/detail.html', context)
