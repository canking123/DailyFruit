from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^add_user/$',views.add_user),
    url(r'^username_repeat/$',views.username_repeat),
    url(r'^login_handle/$', views.login_handle),
    url(r'^login/$',views.login),
    url(r'^logout/$',views.logout),
    url(r'^user_center_info/$', views.user_center_info),
    url(r'^user_center_order/$', views.user_center_order),
    url(r'^user_center_site/$', views.user_center_site),
    url(r'^send/$', views.send),
    url(r'^islogin/$', views.islogin),
    url(r'^active/(\d+)$', views.active),
    url(r'^update_address/$',views.update_address),

]
