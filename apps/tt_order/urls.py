from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^place_order/$', views.place_order),
    url('^do_order/$', views.do_order),
]