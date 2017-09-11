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
    glist = GoodsInfo.objects.filter(gtype_id=l_id)
    count = GoodsInfo.objects.count()

    n_glist = GoodsInfo.objects.all()
    n_glist = n_glist[count - 3:count]

    context = {'glist': glist, 'n_glist': n_glist}
    return render(request, 'tt_goods/list.html', context)


def detail(request, g_id):
    goods = GoodsInfo.objects.filter(id=g_id)
    count = GoodsInfo.objects.count()

    n_glist = GoodsInfo.objects.all()
    n_glist = n_glist[count - 3:count]
    context = {'goods': goods, 'n_glist': n_glist}
    return render(request, 'tt_goods/detail.html', context)
