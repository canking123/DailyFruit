from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^sp/$', views.cart),
    url(r'^add/$', views.add),
    url(r'^count/$', views.count),
]