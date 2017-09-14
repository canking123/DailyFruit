from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^sp/$', views.cart),
    url(r'^add/$', views.add),
    url(r'^count/$', views.count),
    url(r'^add_count/$', views.add_count),
    url(r'^minus_count/$', views.minus_count),
    url(r'^change_count/$', views.change_count),
    url(r'^del_cart/$', views.del_cart),
]