from django.shortcuts import render

# Create your views here.


def cart(request):
    return render(request, 'tt_cart/cart.html')


def add(request):
    pass