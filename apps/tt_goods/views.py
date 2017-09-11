from django.shortcuts import render
from .models import *


# Create your views here.
def index(request):
    # list = []
    # for i in range(1, 7):
    #     glist= GoodsInfo.objects.all().filter(gtype=i)
    #     glist = glist[0:4]
    #     list.append(glist)
    #
    # context = {'glist': list}
    cont={}
    cont2={}

    for i in range(1, 7):
        glist = GoodsInfo.objects.filter(gtype=i)
        glist = glist[0:4]
        cont2 = {'glist%s' % (i): glist}
        cont.update(cont2)

    context = cont
    return render(request, 'tt_goods/index.html', context)


def list(request, l_id):
    glist = GoodsInfo.objects.all().filter(gtype_id=l_id)
    context = {'glist': glist}
    return render(request, 'tt_goods/list.html',context)


def detail(request,g_id):
    goods = GoodsInfo.objects.all().filter(id=g_id)

    context={'goods':goods}
    return render(request, 'tt_goods/detail.html',context)
