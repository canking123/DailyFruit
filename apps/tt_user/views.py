from django.shortcuts import render

# Create your views here.
def register(request):
    return render(request,'tt_user/register.html')
