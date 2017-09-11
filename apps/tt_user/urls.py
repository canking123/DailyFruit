from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^add_user/$',views.add_user),
    url(r'^username_repeat/$',views.username_repeat),
    url(r'^login/$', views.login),
    url(r'^user_center_info/$', views.user_center_info),
    url(r'^user_center_order/$', views.user_center_order),
    url(r'^user_center_site/$', views.user_center_site),
    url(r'^send/$', views.send),
    url(r'^active/$', views.active),
]
