from django.shortcuts import redirect
from django.http import HttpRequest, JsonResponse


# 如果未登录则转向登录页面
def login(func):
    def login_fun(request, *args, **kwargs):
        if 'uid' in request.sessions:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return JsonResponse({'login': 1})
            else:
                return redirect('/user/login')

    return login_fun
