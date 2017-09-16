from django.shortcuts import render
from .models import *
from tt_cart.models import *
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    cont = {}
    cont2 = {}
    for i in range(1, 7):
        glist = GoodsInfo.objects.filter(gtype=i)
        glist = glist[0:4]
        cont2 = {'glist%s' % (i): glist}
        cont.update(cont2)
    context = cont
    return render(request, 'tt_goods/index.html', context)


def list(request, pindex, l_id, l_sort):
    if (l_id == '100'):
        glist = GoodsInfo.objects.all()  # 全部商品
    else:
        glist = GoodsInfo.objects.filter(gtype_id=l_id)  # 筛选一类商品

    if (l_sort == '0'):
        glist = glist.order_by('gtitle')
    elif (l_sort == '1'):
        glist = glist.order_by('gprice')
    elif (l_sort == '2'):
        glist = glist.order_by('gclick')

    gsort = {'num': l_sort}  # 排序方式
    gtype = TypeInfo.objects.filter(id=l_id)  # 一类商品的类型

    count = GoodsInfo.objects.count()  # 总数
    n_glist = GoodsInfo.objects.all()
    n_glist = n_glist[count - 3:count]  # 取出最新的三件商品

    p = Paginator(glist, 15)

<<<<<<< HEAD

    pIndex={'page':pindex,'prepage':int(pindex)-1,'nextpage':int(pindex)+1}#传入的页码
=======
    if (p.page(int(pindex)).has_next()):
        nextpage = int(pindex) + 1
    else:
        nextpage = int(pindex)

    if (p.page(int(pindex)).has_previous()):
        prepage = int(pindex) - 1
    else:
        prepage = int(pindex)

    pIndex = {'page': pindex, 'prepage': prepage, 'nextpage': nextpage}  # 传入的页码
>>>>>>> nsaviour
    glist = p.page(int(pindex))
    plist = p.page_range

    context = {'glist': glist, 'n_glist': n_glist, 'gtype': gtype, 'gsort': gsort, 'plist': plist, 'pIndex': pIndex}
    return render(request, 'tt_goods/list.html', context)


def detail(request, g_id):
    goods = GoodsInfo.objects.filter(id=g_id)  # 取一件商品
    count = GoodsInfo.objects.count()  # 商品总数
    n_glist = GoodsInfo.objects.all()[count - 3:count]  # 取出最新三件商品

    gtype = TypeInfo.objects.filter(goodsinfo__id=g_id)  # 查询商品类型
    context = {'goods': goods, 'n_glist': n_glist, 'gtype': gtype}
    return render(request, 'tt_goods/detail.html', context)

# query：搜索关键字
# page：当前页的page对象
# paginator：分页paginator对象
# def sreach(request,query):
#     return render(request,'search/in')
