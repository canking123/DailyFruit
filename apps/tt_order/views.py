from django.shortcuts import render


# Create your views here.
def place_order(request):
    return render(request,'tt_order/place_order.html')