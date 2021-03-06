# -*- coding:utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpRequest,JsonResponse


def user_login(func):
    def call_func(request, *args, **kwargs):
        # 判断用户是否登录
        if 'uid' in request.session:
            # 如果登录，则继续执行视图
            return func(request, *args, **kwargs)
        else:
            # 如果没有登录，则转到登录页
            if request.is_ajax():
                return JsonResponse({'ok': 1})
            else:
                return redirect('/user/login/')

    return call_func

