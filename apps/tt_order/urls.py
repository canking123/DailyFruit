from django.conf.urls import url

from apps.tt_order import views

urlpatterns = [
    url(r'^place_order/$', views.place_order),
]