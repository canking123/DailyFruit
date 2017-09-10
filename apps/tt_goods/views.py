from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'tt_goods/index.html')
def list(request):
    return render(request,'tt_goods/list.html')
def detail(request):
    return render(request,'tt_goods/detail.html')
